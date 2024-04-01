import sys
import re
from collections import Counter

def parse_log_file(log_file):
    total_requests = 0
    total_data_transmitted = 0
    resources = Counter()
    hosts = Counter()
    status_codes = Counter()

    with open(log_file, 'r') as file:
        for line in file:
            match = re.match(r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+)\s(\S+)\s*(\S*)\s*" (\d{3}) (\d+) "([^"]*)" "([^"]*)"', line)
            if match:
                remote_host = match.group(1)
                resource = match.group(6)
                status_code = match.group(8)
                bytes_transferred = int(match.group(9))

                total_requests += 1
                total_data_transmitted += bytes_transferred
                resources[resource] += 1
                hosts[remote_host] += 1
                status_codes[status_code[0] + 'xx'] += 1

    return total_requests, total_data_transmitted, resources, hosts, status_codes

def print_statistics(log_file):
    total_requests, total_data_transmitted, resources, hosts, status_codes = parse_log_file(log_file)

    print("Total number of requests:", total_requests)
    print("Total data transmitted over all requests:", total_data_transmitted)

    most_requested_resource, resource_count = resources.most_common(1)[0]
    resource_percentage = (resource_count / total_requests) * 100
    print("Most requested resource:", most_requested_resource)
    print("Total number of requests for this resource:", resource_count)
    print("Percentage of requests for this resource:", resource_percentage)

    most_requested_host, host_count = hosts.most_common(1)[0]
    host_percentage = (host_count / total_requests) * 100
    print("Remote host with the most requests:", most_requested_host)
    print("Total number of requests from this remote host:", host_count)
    print("Percentage of requests from this remote host:", host_percentage)

    total_status_codes = sum(status_codes.values())
    for code, count in status_codes.items():
        percentage = (count / total_status_codes) * 100
        print(f"Percentage of {code} status codes:", percentage)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_statistics.py <log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    print_statistics(log_file)

