"""
Part II of the take home technical assignment for
the censys.io interview process. This code looks
at provided data about a host and using the
search.censys.io api searches censys for similar
hosts and returns those hosts.
"""

from censys.search import CensysHosts
import fnmatch
import pprint

pp = pprint.PrettyPrinter(indent=4)


def main():
    """
    Main driving function to generate and eventually print the report.
    """
    host_conn = CensysHosts()

    http_host_ips = ['1.7.184.114', '1.12.52.13', '1.13.0.174', '1.13.190.91', '1.13.250.78', '1.14.49.98', '1.14.131.139', '1.14.142.146', '1.15.139.208', '1.71.161.14', '1.117.98.240', '1.117.115.51', '1.117.166.79', '1.117.188.132', '1.202.41.138', '1.202.249.120', '1.234.65.123', '1.235.191.49', '1.255.4.120', '2.40.116.154', '2.40.116.155', '2.57.104.224', '2.58.68.58', '2.59.41.48', '2.80.42.250', '3.1.36.246', '3.1.116.82', '3.7.255.162', '3.8.243.147', '3.9.6.110', '3.9.96.135', '3.9.230.247', '3.9.236.129', '3.10.49.241', '3.10.86.54', '3.10.189.163', '3.11.20.12', '3.11.30.216', '3.11.109.1', '3.11.124.187', '3.11.132.223', '3.11.147.16', '3.12.69.69', '3.14.161.250', '3.16.13.215', '3.20.14.218', '3.20.47.175', '3.20.90.100', '3.21.60.33', '3.21.243.16']


    report_dict = {
        'HTTPS': {
            "versions": {},
        },
        'HTTP': {
            "versions": {},
        },
    }

    for ip in http_host_ips:
        host = get_host_info(host_conn, ip)
        host_country = get_host_country(host)
        host_services = get_host_services(host)
        update_report(report_dict, host_services, host_country) 
    print_report(report_dict)


def get_host_info(host_conn, ip):
    """
    Returns view info on ip provided by censys view, will raise
    exception if host cannot be obtained.
    """
    host = {}
    try:
        host = host_conn.view(ip)
    except Exception as ex:
        raise(ex)

    return host


def get_host_country(host):
    """
    Attempts to return the country of the host. If host country cannot be
    found, reports UNKNOWN
    """

    host_country = ""
    try:
        host_country = host["location"]["country"]
    except Exception:
        host_country = "UNKNOWN"

    return host_country


def print_report(report_dict):
    """
    Prints out the report information to the console
    """

    print('SIMILAR HOST REPORT:')
    print('versions found:')
    print('     running under http:')
    for version in report_dict['HTTP']["versions"].keys():
        print(f'        version: {version}')
        count = report_dict['HTTP']["versions"][version]["count"]
        countries = report_dict['HTTP']["versions"][version]["countries_found_in"]
        print(f'            count: {count}, countries found in: {list(countries)}')

    print('     running under https:')
    for version in report_dict['HTTPS']["versions"].keys():
        print(f'        version: {version}')
        count = report_dict['HTTPS']["versions"][version]["count"]
        countries = report_dict['HTTPS']["versions"][version]["countries_found_in"]
        print(f'            count: {count}, countries found in: {list(countries)}')
    

# not currently used, was used to get the list of IP addresses initially
def get_http_host_ips(host_conn):
    """
    Retreives IP addresses of hosts with the html_title
    of "Confluence"
    """

    http_hosts = host_conn.search(
        "services.http.response.html_title: Confluence",
        per_page=50,
        pages=1,
        virtual_host="only"
    )

    ip_list = []
    for host in http_hosts():
        ip_list.append(host["ip"])
 
    return ip_list


def get_host_services(host):
    """
    return a list of services running on a host
    """
    services = []
    try:
        services = host["services"]
    except Exception:
        print("failed to get services from host")
        return []

    return services


def update_report(report_dict, host_services, host_country):
    """
    For each given service, filter for HTTP & HTTPS and that confluence is the software
    running. If both are true, extract version and add to list for services running 
    confluence, update value tracking # hosts with service running.
    """
 
    for service in host_services:
        service_name = service["extended_service_name"]
        # filter for http & https

        if not service_name == "HTTPS" and not service_name == "HTTP":
            continue

        if 'response' not in service['http']:
            continue

        if 'body' not in service['http']['response']:
            continue

        if "Confluence" not in service['http']['response']['body']:
            continue
        
        # extract version type from html tags
        pattern = '<meta name="ajs-version-number" content="*">'
        html_tags = service['http']['response']['html_tags']
        software_ver = fnmatch.filter(html_tags, pattern)

        if software_ver:
            version_string = str(software_ver[0])[41:-2]
        else:
            continue

        version_tracker = report_dict[service_name]["versions"]

        # we have seen this version, update counter
        if version_string in version_tracker:
            version_tracker[version_string]["count"] += 1
            version_tracker[version_string]["countries_found_in"].add(host_country)
        # new version, add to dict and initialize value
        else:
            version_tracker[version_string] = {}
            version_tracker[version_string]["count"] = 1
            version_tracker[version_string]["countries_found_in"] = {host_country}


if __name__ == '__main__':
    main()