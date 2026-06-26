#!/usr/bin/env python3
"""
Vultr API v2 Client

A comprehensive client for managing Vultr cloud resources.
Requires API key stored in ~/.config/vultr/api_key

Usage:
    vultr.py <resource> <action> [options]

Resources:
    account         Account info, BGP, bandwidth
    instances       VPS instances (list, create, delete, start, stop, reboot)
    bare-metal      Bare metal servers
    kubernetes      VKE clusters
    databases       Managed databases
    load-balancers  Load balancers
    dns             DNS domains and records
    firewall        Firewall groups and rules
    vpc             VPC networks
    snapshots       Snapshots
    ssh-keys        SSH keys
    regions         Available regions
    plans           Available plans
    object-storage  Object storage (S3-compatible)
    block-storage   Block storage volumes
    reserved-ips    Reserved IP addresses
    iso             ISO images
    backups         Automatic backups
    billing         Billing history and invoices
    tickets         Support tickets
    users           User management

Examples:
    vultr.py account get
    vultr.py instances list
    vultr.py instances get --id abc123
    vultr.py instances create --region ewr --plan vc2-1c-1gb --os 174
    vultr.py instances start --id abc123
    vultr.py dns list
    vultr.py dns records --domain example.com
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

API_BASE = "https://api.vultr.com/v2"


def get_api_key():
    """Load API key from config file."""
    from pathlib import Path
    key_path = Path.home() / ".config" / "vultr" / "api_key"
    if not key_path.exists():
        print(f"Error: API key not found at {key_path}", file=sys.stderr)
        print("Create it with: mkdir -p ~/.config/vultr && echo -n 'YOUR_API_KEY' > ~/.config/vultr/api_key", file=sys.stderr)
        print("Generate API keys at: https://my.vultr.com/settings/#settingsapi", file=sys.stderr)
        sys.exit(1)
    return key_path.read_text().strip()


class VultrClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = API_BASE

    def request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make an API request."""
        url = f"{self.base_url}{endpoint}"
        
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
            if query:
                url = f"{url}?{query}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        body = None
        if data:
            body = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 204:
                    return {"success": True}
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                error_json = json.loads(error_body)
                return {"error": error_json.get("error", error_body), "status": e.code}
            except json.JSONDecodeError:
                return {"error": error_body, "status": e.code}

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        return self.request("POST", endpoint, data=data)

    def patch(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        return self.request("PATCH", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        return self.request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict:
        return self.request("DELETE", endpoint)


def print_json(data: Dict):
    """Pretty print JSON output."""
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Vultr API v2 Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--output", "-o", choices=["json", "table"], default="json", help="Output format")
    
    subparsers = parser.add_subparsers(dest="resource", help="Resource type")

    # Account
    account_parser = subparsers.add_parser("account", help="Account information")
    account_parser.add_argument("action", choices=["get", "bgp", "bandwidth"])

    # Instances
    instances_parser = subparsers.add_parser("instances", help="VPS instances")
    instances_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "start", "stop", "reboot", "reinstall", "bandwidth"])
    instances_parser.add_argument("--id", help="Instance ID")
    instances_parser.add_argument("--region", help="Region ID (e.g., ewr, lax, ams)")
    instances_parser.add_argument("--plan", help="Plan ID (e.g., vc2-1c-1gb)")
    instances_parser.add_argument("--os", type=int, help="OS ID")
    instances_parser.add_argument("--app", type=int, help="Application ID")
    instances_parser.add_argument("--image", help="Image ID (marketplace apps)")
    instances_parser.add_argument("--label", help="Instance label")
    instances_parser.add_argument("--hostname", help="Instance hostname")
    instances_parser.add_argument("--tag", help="Tag")
    instances_parser.add_argument("--tags", nargs="+", help="Multiple tags")
    instances_parser.add_argument("--ipv6", action="store_true", help="Enable IPv6")
    instances_parser.add_argument("--ssh-keys", nargs="+", help="SSH key IDs")
    instances_parser.add_argument("--user-data", help="Base64-encoded user data")
    instances_parser.add_argument("--script", help="Startup script ID")
    instances_parser.add_argument("--reserved-ip", help="Reserved IP ID")
    instances_parser.add_argument("--enable-private-network", action="store_true")
    instances_parser.add_argument("--attach-vpc", nargs="+", help="VPC IDs to attach")

    # Bare Metal
    baremetal_parser = subparsers.add_parser("bare-metal", help="Bare metal servers")
    baremetal_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "start", "stop", "reboot", "reinstall", "bandwidth"])
    baremetal_parser.add_argument("--id", help="Bare metal ID")
    baremetal_parser.add_argument("--region", help="Region ID")
    baremetal_parser.add_argument("--plan", help="Bare metal plan ID")
    baremetal_parser.add_argument("--os", type=int, help="OS ID")
    baremetal_parser.add_argument("--app", type=int, help="Application ID")
    baremetal_parser.add_argument("--label", help="Label")

    # Kubernetes
    k8s_parser = subparsers.add_parser("kubernetes", help="Kubernetes clusters (VKE)")
    k8s_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "kubeconfig", "versions", "node-pools"])
    k8s_parser.add_argument("--id", help="Cluster ID")
    k8s_parser.add_argument("--region", help="Region ID")
    k8s_parser.add_argument("--label", help="Cluster label")
    k8s_parser.add_argument("--version", help="Kubernetes version")
    k8s_parser.add_argument("--node-pool-id", help="Node pool ID")

    # Databases
    db_parser = subparsers.add_parser("databases", help="Managed databases")
    db_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "plans", "usage", "users", "logical-dbs"])
    db_parser.add_argument("--id", help="Database ID")
    db_parser.add_argument("--region", help="Region ID")
    db_parser.add_argument("--plan", help="Database plan")
    db_parser.add_argument("--label", help="Database label")
    db_parser.add_argument("--type", help="Database type (mysql, pg, redis, kafka)")

    # Load Balancers
    lb_parser = subparsers.add_parser("load-balancers", help="Load balancers")
    lb_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    lb_parser.add_argument("--id", help="Load balancer ID")
    lb_parser.add_argument("--region", help="Region ID")
    lb_parser.add_argument("--label", help="Label")

    # DNS
    dns_parser = subparsers.add_parser("dns", help="DNS management")
    dns_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "records", "create-record", "update-record", "delete-record"])
    dns_parser.add_argument("--domain", help="Domain name")
    dns_parser.add_argument("--ip", help="IP address")
    dns_parser.add_argument("--record-id", help="DNS record ID")
    dns_parser.add_argument("--record-type", help="Record type (A, AAAA, CNAME, MX, etc.)")
    dns_parser.add_argument("--record-name", help="Record name")
    dns_parser.add_argument("--record-data", help="Record data/value")
    dns_parser.add_argument("--record-ttl", type=int, help="TTL")
    dns_parser.add_argument("--record-priority", type=int, help="Priority (for MX, SRV)")

    # Firewall
    firewall_parser = subparsers.add_parser("firewall", help="Firewall groups")
    firewall_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "rules", "create-rule", "delete-rule"])
    firewall_parser.add_argument("--id", help="Firewall group ID")
    firewall_parser.add_argument("--description", help="Group description")
    firewall_parser.add_argument("--rule-id", help="Rule ID")
    firewall_parser.add_argument("--ip-type", choices=["v4", "v6"], help="IP type")
    firewall_parser.add_argument("--protocol", choices=["tcp", "udp", "icmp", "gre"], help="Protocol")
    firewall_parser.add_argument("--port", help="Port or port range")
    firewall_parser.add_argument("--subnet", help="Subnet CIDR")
    firewall_parser.add_argument("--subnet-size", type=int, help="Subnet size")

    # VPC
    vpc_parser = subparsers.add_parser("vpc", help="VPC networks")
    vpc_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    vpc_parser.add_argument("--id", help="VPC ID")
    vpc_parser.add_argument("--region", help="Region ID")
    vpc_parser.add_argument("--description", help="VPC description")
    vpc_parser.add_argument("--subnet", help="Subnet CIDR")

    # VPC 2.0
    vpc2_parser = subparsers.add_parser("vpc2", help="VPC 2.0 networks")
    vpc2_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    vpc2_parser.add_argument("--id", help="VPC ID")
    vpc2_parser.add_argument("--region", help="Region ID")
    vpc2_parser.add_argument("--description", help="VPC description")

    # Snapshots
    snapshot_parser = subparsers.add_parser("snapshots", help="Instance snapshots")
    snapshot_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    snapshot_parser.add_argument("--id", help="Snapshot ID")
    snapshot_parser.add_argument("--instance-id", help="Instance ID to snapshot")
    snapshot_parser.add_argument("--description", help="Snapshot description")
    snapshot_parser.add_argument("--url", help="URL to create snapshot from")

    # SSH Keys
    ssh_parser = subparsers.add_parser("ssh-keys", help="SSH keys")
    ssh_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    ssh_parser.add_argument("--id", help="SSH key ID")
    ssh_parser.add_argument("--name", help="SSH key name")
    ssh_parser.add_argument("--key", help="Public SSH key")

    # Regions
    region_parser = subparsers.add_parser("regions", help="Available regions")
    region_parser.add_argument("action", choices=["list", "availability"])
    region_parser.add_argument("--id", help="Region ID")
    region_parser.add_argument("--type", help="Filter by type")

    # Plans
    plan_parser = subparsers.add_parser("plans", help="Available plans")
    plan_parser.add_argument("action", choices=["list", "bare-metal", "region"])
    plan_parser.add_argument("--type", help="Plan type filter")
    plan_parser.add_argument("--region", help="Region ID for availability")
    plan_parser.add_argument("--os", help="OS type filter")

    # Object Storage
    obj_parser = subparsers.add_parser("object-storage", help="Object storage (S3-compatible)")
    obj_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "clusters", "regenerate-keys"])
    obj_parser.add_argument("--id", help="Object storage ID")
    obj_parser.add_argument("--cluster", help="Cluster ID")
    obj_parser.add_argument("--label", help="Label")

    # Block Storage
    block_parser = subparsers.add_parser("block-storage", help="Block storage volumes")
    block_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "attach", "detach"])
    block_parser.add_argument("--id", help="Block storage ID")
    block_parser.add_argument("--region", help="Region ID")
    block_parser.add_argument("--size", type=int, help="Size in GB")
    block_parser.add_argument("--label", help="Label")
    block_parser.add_argument("--instance", help="Instance ID to attach")

    # Reserved IPs
    reserved_parser = subparsers.add_parser("reserved-ips", help="Reserved IP addresses")
    reserved_parser.add_argument("action", choices=["list", "get", "create", "update", "delete", "attach", "detach", "convert"])
    reserved_parser.add_argument("--id", help="Reserved IP ID")
    reserved_parser.add_argument("--region", help="Region ID")
    reserved_parser.add_argument("--ip-type", choices=["v4", "v6"], help="IP type")
    reserved_parser.add_argument("--label", help="Label")
    reserved_parser.add_argument("--instance", help="Instance ID")

    # ISO
    iso_parser = subparsers.add_parser("iso", help="ISO images")
    iso_parser.add_argument("action", choices=["list", "get", "create", "delete", "public"])
    iso_parser.add_argument("--id", help="ISO ID")
    iso_parser.add_argument("--url", help="URL to ISO file")

    # Backups
    backup_parser = subparsers.add_parser("backups", help="Automatic backups")
    backup_parser.add_argument("action", choices=["list", "get"])
    backup_parser.add_argument("--id", help="Backup ID")
    backup_parser.add_argument("--instance", help="Instance ID filter")

    # Billing
    billing_parser = subparsers.add_parser("billing", help="Billing information")
    billing_parser.add_argument("action", choices=["history", "invoices", "invoice", "pending-charges"])
    billing_parser.add_argument("--id", help="Invoice ID")

    # Tickets
    ticket_parser = subparsers.add_parser("tickets", help="Support tickets")
    ticket_parser.add_argument("action", choices=["list", "get", "create", "close"])
    ticket_parser.add_argument("--id", help="Ticket ID")
    ticket_parser.add_argument("--subject", help="Ticket subject")
    ticket_parser.add_argument("--message", help="Ticket message")
    ticket_parser.add_argument("--priority", help="Ticket priority")

    # Users
    user_parser = subparsers.add_parser("users", help="User management")
    user_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    user_parser.add_argument("--id", help="User ID")
    user_parser.add_argument("--email", help="User email")
    user_parser.add_argument("--name", help="User name")
    user_parser.add_argument("--password", help="User password")
    user_parser.add_argument("--api-enabled", type=bool, help="API enabled")

    # Startup Scripts
    script_parser = subparsers.add_parser("scripts", help="Startup scripts")
    script_parser.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    script_parser.add_argument("--id", help="Script ID")
    script_parser.add_argument("--name", help="Script name")
    script_parser.add_argument("--type", choices=["boot", "pxe"], help="Script type")
    script_parser.add_argument("--script", help="Script content")

    # Applications
    app_parser = subparsers.add_parser("applications", help="One-Click and Marketplace applications")
    app_parser.add_argument("action", choices=["list"])
    app_parser.add_argument("--type", choices=["all", "marketplace", "one-click"], help="App type filter")

    # Operating Systems
    os_parser = subparsers.add_parser("os", help="Operating systems")
    os_parser.add_argument("action", choices=["list"])
    os_parser.add_argument("--type", help="OS type filter")

    args = parser.parse_args()

    if not args.resource:
        parser.print_help()
        sys.exit(1)

    # Get API key from config file
    api_key = get_api_key()
    client = VultrClient(api_key)

    # Handle each resource type
    resource = args.resource
    action = args.action

    try:
        result = handle_request(client, resource, action, args)
        print_json(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_request(client: VultrClient, resource: str, action: str, args) -> Dict:
    """Route requests to appropriate API endpoints."""
    
    # Account
    if resource == "account":
        if action == "get":
            return client.get("/account")
        elif action == "bgp":
            return client.get("/account/bgp")
        elif action == "bandwidth":
            return client.get("/account/bandwidth")

    # Instances
    elif resource == "instances":
        if action == "list":
            return client.get("/instances")
        elif action == "get":
            return client.get(f"/instances/{args.id}")
        elif action == "create":
            data = {
                "region": args.region,
                "plan": args.plan,
                "os_id": args.os,
                "app_id": args.app,
                "image_id": args.image,
                "label": args.label,
                "hostname": args.hostname,
                "tag": args.tag,
                "tags": args.tags,
                "enable_ipv6": args.ipv6,
                "sshkey_id": args.ssh_keys,
                "user_data": args.user_data,
                "script_id": args.script,
                "reserved_ipv4": args.reserved_ip,
                "attach_vpc": args.attach_vpc,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/instances", data)
        elif action == "update":
            data = {"label": args.label, "tags": args.tags}
            data = {k: v for k, v in data.items() if v is not None}
            return client.patch(f"/instances/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/instances/{args.id}")
        elif action == "start":
            return client.post(f"/instances/{args.id}/start")
        elif action == "stop":
            return client.post(f"/instances/{args.id}/halt")
        elif action == "reboot":
            return client.post(f"/instances/{args.id}/reboot")
        elif action == "reinstall":
            data = {"hostname": args.hostname} if args.hostname else {}
            return client.post(f"/instances/{args.id}/reinstall", data)
        elif action == "bandwidth":
            return client.get(f"/instances/{args.id}/bandwidth")

    # Bare Metal
    elif resource == "bare-metal":
        if action == "list":
            return client.get("/bare-metals")
        elif action == "get":
            return client.get(f"/bare-metals/{args.id}")
        elif action == "create":
            data = {
                "region": args.region,
                "plan": args.plan,
                "os_id": args.os,
                "app_id": args.app,
                "label": args.label,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/bare-metals", data)
        elif action == "update":
            data = {"label": args.label}
            data = {k: v for k, v in data.items() if v is not None}
            return client.patch(f"/bare-metals/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/bare-metals/{args.id}")
        elif action == "start":
            return client.post(f"/bare-metals/{args.id}/start")
        elif action == "stop":
            return client.post(f"/bare-metals/{args.id}/halt")
        elif action == "reboot":
            return client.post(f"/bare-metals/{args.id}/reboot")
        elif action == "reinstall":
            return client.post(f"/bare-metals/{args.id}/reinstall")
        elif action == "bandwidth":
            return client.get(f"/bare-metals/{args.id}/bandwidth")

    # Kubernetes
    elif resource == "kubernetes":
        if action == "list":
            return client.get("/kubernetes/clusters")
        elif action == "get":
            return client.get(f"/kubernetes/clusters/{args.id}")
        elif action == "create":
            data = {
                "region": args.region,
                "label": args.label,
                "version": args.version,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/kubernetes/clusters", data)
        elif action == "update":
            data = {"label": args.label}
            return client.put(f"/kubernetes/clusters/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/kubernetes/clusters/{args.id}")
        elif action == "kubeconfig":
            return client.get(f"/kubernetes/clusters/{args.id}/kubeconfig")
        elif action == "versions":
            return client.get("/kubernetes/versions")
        elif action == "node-pools":
            if args.node_pool_id:
                return client.get(f"/kubernetes/clusters/{args.id}/node-pools/{args.node_pool_id}")
            return client.get(f"/kubernetes/clusters/{args.id}/node-pools")

    # Databases
    elif resource == "databases":
        if action == "list":
            return client.get("/managed-databases")
        elif action == "plans":
            return client.get("/managed-databases/plans")
        elif action == "get":
            return client.get(f"/managed-databases/{args.id}")
        elif action == "create":
            data = {
                "region": args.region,
                "plan": args.plan,
                "label": args.label,
                "database_type": args.type,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/managed-databases", data)
        elif action == "update":
            data = {"label": args.label}
            return client.put(f"/managed-databases/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/managed-databases/{args.id}")
        elif action == "usage":
            return client.get(f"/managed-databases/{args.id}/usage")
        elif action == "users":
            return client.get(f"/managed-databases/{args.id}/users")
        elif action == "logical-dbs":
            return client.get(f"/managed-databases/{args.id}/logical-databases")

    # Load Balancers
    elif resource == "load-balancers":
        if action == "list":
            return client.get("/load-balancers")
        elif action == "get":
            return client.get(f"/load-balancers/{args.id}")
        elif action == "create":
            data = {"region": args.region, "label": args.label}
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/load-balancers", data)
        elif action == "update":
            data = {"label": args.label}
            return client.patch(f"/load-balancers/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/load-balancers/{args.id}")

    # DNS
    elif resource == "dns":
        if action == "list":
            return client.get("/domains")
        elif action == "get":
            return client.get(f"/domains/{args.domain}")
        elif action == "create":
            data = {"domain": args.domain, "ip": args.ip}
            return client.post("/domains", data)
        elif action == "delete":
            return client.delete(f"/domains/{args.domain}")
        elif action == "records":
            return client.get(f"/domains/{args.domain}/records")
        elif action == "create-record":
            data = {
                "name": args.record_name,
                "type": args.record_type,
                "data": args.record_data,
                "ttl": args.record_ttl,
                "priority": args.record_priority,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post(f"/domains/{args.domain}/records", data)
        elif action == "update-record":
            data = {
                "name": args.record_name,
                "data": args.record_data,
                "ttl": args.record_ttl,
                "priority": args.record_priority,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.patch(f"/domains/{args.domain}/records/{args.record_id}", data)
        elif action == "delete-record":
            return client.delete(f"/domains/{args.domain}/records/{args.record_id}")

    # Firewall
    elif resource == "firewall":
        if action == "list":
            return client.get("/firewalls")
        elif action == "get":
            return client.get(f"/firewalls/{args.id}")
        elif action == "create":
            data = {"description": args.description}
            return client.post("/firewalls", data)
        elif action == "update":
            data = {"description": args.description}
            return client.put(f"/firewalls/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/firewalls/{args.id}")
        elif action == "rules":
            return client.get(f"/firewalls/{args.id}/rules")
        elif action == "create-rule":
            data = {
                "ip_type": args.ip_type,
                "protocol": args.protocol,
                "port": args.port,
                "subnet": args.subnet,
                "subnet_size": args.subnet_size,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post(f"/firewalls/{args.id}/rules", data)
        elif action == "delete-rule":
            return client.delete(f"/firewalls/{args.id}/rules/{args.rule_id}")

    # VPC
    elif resource == "vpc":
        if action == "list":
            return client.get("/vpcs")
        elif action == "get":
            return client.get(f"/vpcs/{args.id}")
        elif action == "create":
            data = {"region": args.region, "description": args.description, "subnet": args.subnet}
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/vpcs", data)
        elif action == "update":
            data = {"description": args.description}
            return client.put(f"/vpcs/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/vpcs/{args.id}")

    # VPC 2.0
    elif resource == "vpc2":
        if action == "list":
            return client.get("/vpc2")
        elif action == "get":
            return client.get(f"/vpc2/{args.id}")
        elif action == "create":
            data = {"region": args.region, "description": args.description}
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/vpc2", data)
        elif action == "update":
            data = {"description": args.description}
            return client.put(f"/vpc2/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/vpc2/{args.id}")

    # Snapshots
    elif resource == "snapshots":
        if action == "list":
            return client.get("/snapshots")
        elif action == "get":
            return client.get(f"/snapshots/{args.id}")
        elif action == "create":
            if args.url:
                return client.post("/snapshots/create-from-url", {"url": args.url})
            data = {"instance_id": args.instance_id, "description": args.description}
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/snapshots", data)
        elif action == "update":
            return client.put(f"/snapshots/{args.id}", {"description": args.description})
        elif action == "delete":
            return client.delete(f"/snapshots/{args.id}")

    # SSH Keys
    elif resource == "ssh-keys":
        if action == "list":
            return client.get("/ssh-keys")
        elif action == "get":
            return client.get(f"/ssh-keys/{args.id}")
        elif action == "create":
            data = {"name": args.name, "ssh_key": args.key}
            return client.post("/ssh-keys", data)
        elif action == "update":
            data = {"name": args.name}
            return client.patch(f"/ssh-keys/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/ssh-keys/{args.id}")

    # Regions
    elif resource == "regions":
        if action == "list":
            return client.get("/regions")
        elif action == "availability":
            return client.get(f"/regions/{args.id}/availability", {"type": args.type})

    # Plans
    elif resource == "plans":
        if action == "list":
            return client.get("/plans", {"type": args.type})
        elif action == "bare-metal":
            return client.get("/plans-metal")
        elif action == "region":
            return client.get(f"/regions/{args.region}/availability")

    # Object Storage
    elif resource == "object-storage":
        if action == "list":
            return client.get("/object-storage")
        elif action == "get":
            return client.get(f"/object-storage/{args.id}")
        elif action == "create":
            data = {"cluster_id": args.cluster, "label": args.label}
            return client.post("/object-storage", data)
        elif action == "update":
            return client.put(f"/object-storage/{args.id}", {"label": args.label})
        elif action == "delete":
            return client.delete(f"/object-storage/{args.id}")
        elif action == "clusters":
            return client.get("/object-storage/clusters")
        elif action == "regenerate-keys":
            return client.post(f"/object-storage/{args.id}/regenerate-keys")

    # Block Storage
    elif resource == "block-storage":
        if action == "list":
            return client.get("/blocks")
        elif action == "get":
            return client.get(f"/blocks/{args.id}")
        elif action == "create":
            data = {"region": args.region, "size_gb": args.size, "label": args.label}
            return client.post("/blocks", data)
        elif action == "update":
            data = {"label": args.label, "size_gb": args.size}
            return client.patch(f"/blocks/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/blocks/{args.id}")
        elif action == "attach":
            return client.post(f"/blocks/{args.id}/attach", {"instance_id": args.instance})
        elif action == "detach":
            return client.post(f"/blocks/{args.id}/detach")

    # Reserved IPs
    elif resource == "reserved-ips":
        if action == "list":
            return client.get("/reserved-ips")
        elif action == "get":
            return client.get(f"/reserved-ips/{args.id}")
        elif action == "create":
            data = {"region": args.region, "ip_type": args.ip_type, "label": args.label}
            return client.post("/reserved-ips", data)
        elif action == "update":
            return client.patch(f"/reserved-ips/{args.id}", {"label": args.label})
        elif action == "delete":
            return client.delete(f"/reserved-ips/{args.id}")
        elif action == "attach":
            return client.post(f"/reserved-ips/{args.id}/attach", {"instance_id": args.instance})
        elif action == "detach":
            return client.post(f"/reserved-ips/{args.id}/detach")
        elif action == "convert":
            return client.post(f"/reserved-ips/{args.id}/convert", {"instance_id": args.instance})

    # ISO
    elif resource == "iso":
        if action == "list":
            return client.get("/iso")
        elif action == "get":
            return client.get(f"/iso/{args.id}")
        elif action == "create":
            return client.post("/iso", {"url": args.url})
        elif action == "delete":
            return client.delete(f"/iso/{args.id}")
        elif action == "public":
            return client.get("/iso-public")

    # Backups
    elif resource == "backups":
        if action == "list":
            return client.get("/backups", {"instance_id": args.instance})
        elif action == "get":
            return client.get(f"/backups/{args.id}")

    # Billing
    elif resource == "billing":
        if action == "history":
            return client.get("/billing/history")
        elif action == "invoices":
            return client.get("/invoices")
        elif action == "invoice":
            return client.get(f"/invoices/{args.id}")
        elif action == "pending-charges":
            return client.get("/billing/pending-charges")

    # Tickets
    elif resource == "tickets":
        if action == "list":
            return client.get("/tickets")
        elif action == "get":
            return client.get(f"/tickets/{args.id}")
        elif action == "create":
            data = {"subject": args.subject, "message": args.message, "priority": args.priority}
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/tickets", data)
        elif action == "close":
            return client.post(f"/tickets/{args.id}/close")

    # Users
    elif resource == "users":
        if action == "list":
            return client.get("/users")
        elif action == "get":
            return client.get(f"/users/{args.id}")
        elif action == "create":
            data = {
                "email": args.email,
                "name": args.name,
                "password": args.password,
                "api_enabled": args.api_enabled,
            }
            data = {k: v for k, v in data.items() if v is not None}
            return client.post("/users", data)
        elif action == "update":
            data = {"email": args.email, "name": args.name, "api_enabled": args.api_enabled}
            data = {k: v for k, v in data.items() if v is not None}
            return client.patch(f"/users/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/users/{args.id}")

    # Startup Scripts
    elif resource == "scripts":
        if action == "list":
            return client.get("/startup-scripts")
        elif action == "get":
            return client.get(f"/startup-scripts/{args.id}")
        elif action == "create":
            data = {"name": args.name, "type": args.type, "script": args.script}
            return client.post("/startup-scripts", data)
        elif action == "update":
            data = {"name": args.name, "script": args.script}
            return client.patch(f"/startup-scripts/{args.id}", data)
        elif action == "delete":
            return client.delete(f"/startup-scripts/{args.id}")

    # Applications
    elif resource == "applications":
        return client.get("/applications", {"type": args.type})

    # Operating Systems
    elif resource == "os":
        return client.get("/os")

    return {"error": f"Unknown resource/action: {resource}/{action}"}


if __name__ == "__main__":
    main()
