import sys
import dns.query
from dns.exception import DNSException
import datetime
import time
import logging

logging.basicConfig(level=logging.WARNING)

## Root server ips
def root_servers_ips():
    return ['198.41.0.4','199.9.14.201','192.33.4.12','199.7.91.13','192.203.230.10','192.5.5.241','192.112.36.4','198.97.190.53','192.36.148.17','192.58.128.30','193.0.14.129','199.7.83.42','202.12.27.33']

#Split the domain into sub domains
def split_domain(domain):
    return domain.split('.')

#Iteratively resolves the ips for each sub_domain
def resolveDomain(domain,servers,rdtype):
    n = split_domain(domain)
    my_servers = servers
    #We loop over each subdomain for eg { '.','.com','google.com'}
    for i in range(len(n), 0, -1):
        sub_domain = '.'.join(n[i-1:])
        # print(sub_domain)
        next_servers = _resolveDomain(sub_domain,my_servers,rdtype)
        my_servers = next_servers
    return my_servers

#This is the recursive function we call whenvever we want to resolve the domain
def _resolveDomain(sub_domain, my_servers, rdtype):
    dns_name = dns.name.from_text(sub_domain)
    response = get_next_server(dns_name,my_servers,rdtype)
    # print('XYZ1',response)
    #Case when the response has answer
    if len(response.answer) > 0: 
        return response.answer[0].to_text().split(" ")[-1]
    #Case when we get SOA in authority response
    elif ((len(response.authority) > 0) and (response.authority[0].rdtype == dns.rdatatype.SOA)):
        #We set the same server for next round as well
        return my_servers
    #Case to parse ips from the additional for NS in authority
    elif len(response.authority)>0 and len(response.additional)>0:
        duh_servers = get_ip_from_ns(response,dns_name)
        # print('XYZ2',duh_servers)
        return duh_servers
    else:
        #This is to handle the special edge case of google.co.jp
        ns_names = get_ns_from_authority(response,dns_name) #ns1.google.com.
        # print("XYZ3", ns_names)
        something = []
        for name in ns_names:
            something = resolveDomain(name,root_servers_ips(),rdtype)
            # print("XYZ4",something)
            if something:
                break
        # next_servers = get_next_server(sub_domain,[something],rdtype).answer[0].to_text().split(" ")[-1]
        return [something]

#Helper funciton to parse the ip from the response for NS serveres
def get_ip_from_ns(response,dns_name):
    ns_names = get_ns_from_authority(response,dns_name)
    list_of_ips = ip_for_ns_from_additional(response,ns_names)
    list_1=[]
    for k,v in list_of_ips.items():
        list_1.append(v)
    return list_1

#Function to reoslve the next servers for a particular domain.
def get_next_server(dns_name,servers,type):
    response = None
    for server in servers:
        response = resolve(dns_name,server, type)
        if response:
            break
    return response

#Helper function
def get_ns_from_authority(response,dns_name):
    ns_names = []
    try:
        ns_rrset = response.find_rrset(response.authority, dns_name, dns.rdataclass.IN, dns.rdatatype.NS)
        for rr in ns_rrset:
            ns_names.append(rr.to_text())
    except KeyError:
        logging.debug('Invalid Key')
    return ns_names

#Helper function 
def ip_for_ns_from_additional(response,ns_names):
    ns_ips = {}
    for name in ns_names:
        somename = dns.name.from_text(name)
        try:
            #Using find_rrset to find the requiered data from rr_set
            ns_rrset = response.find_rrset(response.additional, somename, dns.rdataclass.IN, dns.rdatatype.A)
            for rr in ns_rrset:
                ns_ips[name] = rr.to_text()
        except KeyError:
            logging.debug('Invalid Key')
    return ns_ips

#Resolves the query using dnspython functions
def resolve(dns_name,server,rdatatype):
    query = dns.message.make_query(dns_name, rdatatype)
    response = dns.query.udp(query,server)
    return response

#Convert the output to final response format
def beautify_output(result, type, query_time):
	if(len(result.answer)>0):
		rrset = result.answer[0]
		rr = rrset[0]	
		if(type == "A" and rr.rdtype == dns.rdatatype.CNAME):
			cname_ans = resolveDomain(str(rr),root_servers_ips(), dns.rdatatype.from_text("A"))
			result.answer += cname_ans.answer

	output = ""

	output += "QUESTION SECTION:\n" + result.question[0].to_text() + "\n\n" + "ANSWER SECTION:\n"

	for ans in result.answer:
		output += ans.to_text()+"\n"

	output += "\n" + "Query Time: "
	output += str(query_time) + " sec\n"

	currentDT = datetime.datetime.now()
	output += currentDT.strftime("%a %b %d %H:%M:%S %Y\n")

	output += "MSG SIZE rcvd: " + str(sys.getsizeof(result))

	return output

#Main function
if __name__ == "__main__":
    domain_name = sys.argv[1]
    type = sys.argv[2]
    servers = root_servers_ips()
    domain = domain_name.replace("www.","")
    start_time = time.time()
    rdtype = dns.rdatatype.from_text(type)
    answer = resolveDomain(domain,servers,rdtype)
    for ans in answer:
        finalanswer = resolve(domain,ans,type)
        if finalanswer:
            break
    end_time = time.time()
    print("Final Answer",beautify_output(finalanswer,type,end_time-start_time))
