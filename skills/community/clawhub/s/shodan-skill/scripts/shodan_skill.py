#!/usr/bin/env python3
import sys
import json
import shodan
import os
import argparse

# Try to get API key from environment or config file
API_KEY = os.environ.get('SHODAN_API_KEY')
CONFIG_FILE = os.path.expanduser('~/.config/shodan/api_key')

if not API_KEY:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                API_KEY = f.read().strip()
        except:
            pass

if not API_KEY:
    print(json.dumps({"error": "Shodan API key not found. Please set SHODAN_API_KEY env var or run 'shodan init <key>'"}))
    sys.exit(1)

try:
    api = shodan.Shodan(API_KEY)
except Exception as e:
    print(json.dumps({"error": f"Failed to initialize Shodan API: {str(e)}"}))
    sys.exit(1)

def cmd_host(args):
    try:
        host = api.host(args.ip, history=args.history, minify=args.minify)
        print(json.dumps(host, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_search(args):
    try:
        limit = args.limit if args.limit else 20
        page = args.page if args.page else 1
        results = api.search(args.query, limit=limit, page=page, facets=args.facets)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_count(args):
    try:
        results = api.count(args.query, facets=args.facets)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_scan(args):
    try:
        scan = api.scan(args.ips)
        print(json.dumps(scan, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_alert_list(args):
    try:
        alerts = api.alerts()
        print(json.dumps(alerts, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_alert_create(args):
    try:
        # Create alert for a network range or IP
        alert = api.create_alert(args.name, args.ip)
        print(json.dumps(alert, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_alert_info(args):
    try:
        info = api.alert_info(args.id)
        print(json.dumps(info, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_dns_domain(args):
    try:
        domain = api.dns.domain_info(args.domain)
        print(json.dumps(domain, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_dns_resolve(args):
    try:
        hostnames = args.hostnames.split(',')
        resolved = api.dns.resolve(hostnames)
        print(json.dumps(resolved, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_profile(args):
    try:
        profile = api.info()
        print(json.dumps(profile, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_myip(args):
    try:
        ip = api.tools.myip()
        print(json.dumps({"ip": ip}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_ports(args):
    try:
        ports = api.ports()
        print(json.dumps(ports, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_protocols(args):
    try:
        protocols = api.protocols()
        print(json.dumps(protocols, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_query_search(args):
    try:
        results = api.queries(query=args.query)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_query_tags(args):
    try:
        tags = api.query_tags(size=args.limit)
        print(json.dumps(tags, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_notifier_list(args):
    try:
        notifiers = api.notifiers()
        print(json.dumps(notifiers, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_exploit_search(args):
    try:
        # Note: Exploit API usually requires separate subscription or Enterprise?
        # The python lib has api.exploits.search()
        results = api.exploits.search(args.query, limit=args.limit)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_filters(args):
    # Hardcoded list of common filters from https://www.shodan.io/search/filters
    filters = {
        "General": ["after", "before", "asn", "city", "country", "geo", "hash", "has_ipv6", "has_screenshot", "hostname", "ip", "isp", "net", "org", "os", "port", "postal", "product", "region", "state", "version", "vuln"],
        "HTTP": ["http.component", "http.component_category", "http.favicon.hash", "http.html", "http.html_hash", "http.robots_hash", "http.securitytxt", "http.status", "http.title", "http.waf"],
        "SSL/TLS": ["ssl", "ssl.alpn", "ssl.cert.alg", "ssl.cert.expired", "ssl.cert.extension", "ssl.cert.fingerprint", "ssl.cert.issuer.cn", "ssl.cert.pubkey.bits", "ssl.cert.serial", "ssl.cert.subject.cn", "ssl.chain_count", "ssl.cipher.bits", "ssl.cipher.name", "ssl.cipher.version", "ssl.ja3s", "ssl.jarm", "ssl.version"],
        "Cloud": ["cloud.provider", "cloud.region", "cloud.service"],
        "Telnet": ["telnet.option", "telnet.do", "telnet.dont", "telnet.will", "telnet.wont"],
        "NTP": ["ntp.op_code"],
        "SSH": ["ssh.cipher", "ssh.fingerprint", "ssh.hassh", "ssh.kex", "ssh.mac", "ssh.type"],
        "Screenshot": ["screenshot.label"]
    }
    print(json.dumps(filters, indent=2))

def cmd_datapedia(args):
    # Simplified Datapedia structure
    datapedia = {
        "ip_str": "IP address as a string",
        "port": "Port number",
        "transport": "Transport protocol (tcp/udp)",
        "data": "Main banner data",
        "hostnames": "List of hostnames",
        "domains": "List of domains",
        "location": {
            "city": "City name",
            "country_name": "Country name",
            "country_code": "2-letter country code",
            "latitude": "Latitude",
            "longitude": "Longitude"
        },
        "org": "Organization name",
        "isp": "ISP name",
        "asn": "Autonomous System Number",
        "os": "Operating System",
        "http": {
            "title": "Website title",
            "html": "HTML content",
            "server": "Server header",
            "status": "HTTP status code",
            "favicon": "Favicon data (hash, location)"
        },
        "ssl": {
            "cert": "Certificate details",
            "cipher": "Cipher details",
            "versions": "Supported SSL/TLS versions"
        },
        "cpe": "Common Platform Enumeration",
        "vulns": "List of vulnerabilities (CVEs)"
    }
    print(json.dumps(datapedia, indent=2))

def cmd_stream(args):
    try:
        limit = args.limit if args.limit else 10
        count = 0
        
        if args.ports:
            stream = api.stream.ports(args.ports.split(','))
        elif args.alert:
            stream = api.stream.alert(args.alert)
        else:
            stream = api.stream.banners()

        print(f"[*] Streaming {limit} banners...", file=sys.stderr)
        
        for banner in stream:
            print(json.dumps(banner))
            count += 1
            if count >= limit:
                break
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def cmd_trends(args):
    try:
        # Use facets for trends
        results = api.count(args.query, facets=args.facets)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def main():
    parser = argparse.ArgumentParser(description="Shodan Pro Skill CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Host
    host_parser = subparsers.add_parser("host", help="Get host details")
    host_parser.add_argument("ip", help="IP address")
    host_parser.add_argument("--history", action="store_true", help="Show history")
    host_parser.add_argument("--minify", action="store_true", help="Minify response")

    # Search
    search_parser = subparsers.add_parser("search", help="Search Shodan")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, help="Limit results")
    search_parser.add_argument("--page", type=int, help="Page number")
    search_parser.add_argument("--facets", help="Facets (comma separated, e.g. country,org)")

    # Count
    count_parser = subparsers.add_parser("count", help="Count results")
    count_parser.add_argument("query", help="Search query")
    count_parser.add_argument("--facets", help="Facets for stats")

    # Stream
    stream_parser = subparsers.add_parser("stream", help="Stream realtime data")
    stream_parser.add_argument("--ports", help="Ports to filter")
    stream_parser.add_argument("--alert", help="Alert ID to filter")
    stream_parser.add_argument("--limit", type=int, default=10, help="Stop after N banners")

    # Trends (Alias for count+facets)
    trends_parser = subparsers.add_parser("trends", help="Get trends (facets)")
    trends_parser.add_argument("query", help="Search query")
    trends_parser.add_argument("--facets", help="Facets", default="country,org,os,product,port")

    # Scan
    scan_parser = subparsers.add_parser("scan", help="Request on-demand scan")
    scan_parser.add_argument("ips", help="IP or list of IPs/CIDRs")
    if ',' in sys.argv: # Hacky check, but argparse handles it if we just pass strings
        pass

    # Alerts
    alert_list_parser = subparsers.add_parser("alert_list", help="List alerts")
    
    alert_create_parser = subparsers.add_parser("alert_create", help="Create alert")
    alert_create_parser.add_argument("name", help="Alert name")
    alert_create_parser.add_argument("ip", help="IP/CIDR block to monitor")

    alert_info_parser = subparsers.add_parser("alert_info", help="Get alert info")
    alert_info_parser.add_argument("id", help="Alert ID")

    # DNS
    dns_domain_parser = subparsers.add_parser("dns_domain", help="Get domain info")
    dns_domain_parser.add_argument("domain", help="Domain name")

    dns_resolve_parser = subparsers.add_parser("dns_resolve", help="Resolve hostnames")
    dns_resolve_parser.add_argument("hostnames", help="Comma separated hostnames")

    # Profile & Tools
    subparsers.add_parser("profile", help="Get account profile/info")
    subparsers.add_parser("myip", help="Get my IP")
    subparsers.add_parser("ports", help="List ports Shodan scans")
    subparsers.add_parser("protocols", help="List protocols Shodan scans")

    # Directory
    query_search_parser = subparsers.add_parser("query_search", help="Search saved queries")
    query_search_parser.add_argument("query", help="Query string")
    
    query_tags_parser = subparsers.add_parser("query_tags", help="List popular tags")
    query_tags_parser.add_argument("--limit", type=int, default=10, help="Number of tags")

    # Notifiers
    subparsers.add_parser("notifier_list", help="List notifiers")
    
    # Exploits
    exploit_search_parser = subparsers.add_parser("exploit_search", help="Search exploits")
    exploit_search_parser.add_argument("query", help="Search query")
    exploit_search_parser.add_argument("--limit", type=int, default=10, help="Limit results")

    # Cheat Sheets
    subparsers.add_parser("filters", help="List common search filters")
    subparsers.add_parser("datapedia", help="List common banner fields")

    args = parser.parse_args()

    if args.command == "host":
        cmd_host(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "count":
        cmd_count(args)
    elif args.command == "stream":
        cmd_stream(args)
    elif args.command == "trends":
        cmd_trends(args)
    elif args.command == "scan":
        if ',' in args.ips:
             args.ips = args.ips.split(',')
        cmd_scan(args)
    elif args.command == "alert_list":
        cmd_alert_list(args)
    elif args.command == "alert_create":
        cmd_alert_create(args)
    elif args.command == "alert_info":
        cmd_alert_info(args)
    elif args.command == "dns_domain":
        cmd_dns_domain(args)
    elif args.command == "dns_resolve":
        cmd_dns_resolve(args)
    elif args.command == "profile":
        cmd_profile(args)
    elif args.command == "myip":
        cmd_myip(args)
    elif args.command == "ports":
        cmd_ports(args)
    elif args.command == "protocols":
        cmd_protocols(args)
    elif args.command == "query_search":
        cmd_query_search(args)
    elif args.command == "query_tags":
        cmd_query_tags(args)
    elif args.command == "notifier_list":
        cmd_notifier_list(args)
    elif args.command == "exploit_search":
        cmd_exploit_search(args)
    elif args.command == "filters":
        cmd_filters(args)
    elif args.command == "datapedia":
        cmd_datapedia(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
