---------------------------------------
# DNS Resolver using iterative queries.

This tool is an implementation for the DNS resolver which can iterativetly resolve domains by first contacting the root server, then the top-level domains, all the way down to the corresponding name server to resolve the DNS query. We have also performed an indepth comparion study of the performance of this tool compared to other DNS resolvers like Google DNS(8.8.8.8) and local DNS Server deployed at Stony Brook University.

DNSSec: The Domain Name System Security Extensions (DNSSEC) is a feature of the Domain Name System (DNS) that authenticates responses to domain name lookups. It does not provide privacy protections for those lookups, but prevents attackers from manipulating or poisoning the responses to DNS requests

----------
## Features:

- It can handle NS, MX, CNAME name reslutions apart form the A type request.
- It can handle urls like google.co.jp which often does not resolve to IP address in one pass
- It also supports IP resolution for DNSsec protocol.

------------------------------
## Platform : 

python - 2.7.16

-------------------------------
## Libaries Used :

dnspython - 2.1.0

cryptography - 35.0.0

------------------------
## Main Files:

mydig.py : For DNS reesolution of domains for types including A, MX, NS, CNAME

mydig_dnssec.py : For DNS resoltion of domains with DNSSec enabled for types including A, MX, NS, CNAME

--------------------
## Setup : 

1. dnspython needs to be installed
    
       Command: pip install dnspython

2. cryptography needs to be installed

       Command: pip install cryptography

-------------------------
## To run the program:

A) To run mydig.py for DNS resolution

    python mydig.py [domain] [type]

    Eg: python mydig.py cnn.com A

B) To run mydig_dnssec.py for DNSSec protocl enabled sites resolution

    python mydig_dnssec.py [domain] [type]

    Eg: python mydig.py verisigninc.com A
