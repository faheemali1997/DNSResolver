---------------------------------------
DNS Resolver using iterative queries.

This tool is an implementation for the DNS resolver which can iterativetly resolve domains by first contacting the root server, then the top-level domains, all the way down to the corresponding name server to resolve the DNS query. We have also performed an indepth comparion study of the performance of this tool compared to other DNS resolvers like Google DNS(8.8.8.8) and local DNS Server deployed at Stony Brook University.

----------
Features:
> It can handle NS, MX, CNAME name reslutions apart form the A type request.
> It can handle urls like google.co.jp which often does not resolve to IP address in one pass
> It also supports IP resolution for DNSsec protocol.

------------------------------


Libaries Used : dnspython, cryptography

--------------------
Setup : 

1. dnspython needs to be installed
    
    Command: pip install dnspython

2. cryptography needs to be installed

    Command: pip install cryptography

-------------------------
** To run the program: **

A) To run mydig.py for DNS resolution

    python mydig.py [domain] [type]

    Eg: python mydig.py cnn.com A

B) To run mydig_dnssec.py for DNSSec protocl enabled sites resolution

    python mydig_dnssec.py [domain] [type]

    Eg: python mydig.py verisigninc.com A

==========================================================================================
