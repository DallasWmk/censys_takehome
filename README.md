# README
Created: 2023-02-1411:38

## Introduction
The code included in this repo is for the censys take home technical assessment. Included in the `notes.md` file is the answer to and description of how I arrived at that answer for Part I, the research portion of the take home assessment.

The `development_report.txt` file contains the output of the program for your convenience, however, should you decide to run the program yourself, it can be run with the command: `python3 find_similar_hosts.py` . The program currently takes no arguments, but could be adapted in the future to allow for more flexible use cases.

## Program Description
The research from Part I showed that the host had only one port open (port 80) running HTTP with a confluence instance version 7.13.2 running. The program searches for hosts whom return a services.http.html_title of "Confluence" and then begins to extract the version of confluence that is running, along with the country that the host is in. The output of the program is divided into two portions, the HTTP services running some version of confluence including the number of hosts (of the 50 scanned) that are running that version, and the countries that those hosts were found in, and the same info but for HTTPS.

## Analysis Description
The analysis of the program output shows the countries discovered in the scan that has hosts running versions of confluence that are vulnerable to cve-2022-26134. The analysis goes further to break down of the 50 hosts scanned, how many of them are running vulnerable versions, then displays the vulnerability host percentage by country. The goal of this analysis was to act as a vulnerability report on a small sample of what potentially could be businesses in a given country.

