# Censys Take Home Technical
Created: 2023-02-1308:06

## Description
- Three parts
- Research
- Development
- Light Analysis
- Research
- Discover service running on remote host and its version
- Initial thoughts:
- If the host is live see if it can be scanned by nmap
- detection does not appear to be an issue, aggressive scans should find what we are looking for.
- Manually looking at files may be required if host is not live
- Development
- Using the provided censys API
- find hosts that are similar to that of the host in the recon phase
- Initial thoughts:
- once the data comes back from the research portion, interacting with the API to find similar hosts should be easy. The more data found in phase 1 the better the report that can be generated here.
- Light Analysis
- Break down host statistics by HTTP/HTTPS and one or more interesting characteristics

## Part I: Research
### Provided file
- Unzipping the provided file gives us:
- folder containing:
- CSS Files
- JS Files
- html file
- appear to be a saved result from search.censys for the given host
- banner  for 80/HTTP shows that the server is NGINX
### Manual Interaction
- host irresponsive to ping
- whois page has invalid contact info
- in the `services.http.response.body` of the `seach.censys.io` results page shows an `ajs-verion-number` of 7.13.2
- this corresponds to confluence version 7.13.2
- exploitDB shows no exploits however,
- research shows that this version _may_ be vulnerable to CVE-2022-26134 (critical RCE vulnerability)
### NMAP Scan
- command ran: `nmap -v -A -T5 114.119.117.220`
- results:
- port 80 open running HTTP via nginx
- host is running Oracle Virtualbox (possibly, results may vary w/ OS scans)

### Results:
- Host (nmap report): Oracle Virtualbox
- location: china
- Port Status: 80 (http) open, all others appear in a filtered state
- version running is `nginx`
- attempting to connect via web browser results in `502 bad gateway`
- although host is reported as up
- webservice hosted:  Atlassian Confluence
- webservice version: 7.13.2
- Based on provided `search.censys.io` results page the webpage is hosting a confluence instance version 7.13.2 which according to https://nvd.nist.gov/vuln/detail/cve-2022-26134 is a vulnerable version

## Part II Development
- set up account with censys to access api
- search criteria
- `services.http.response.html_title: Confluence`
- final report format
- list found versions
- count of # of hosts with that version
- count # of _services_ with that version