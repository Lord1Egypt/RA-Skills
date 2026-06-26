#!/usr/bin/env python3
"""CIDR/Subnet calculator for network engineers and developers.

Calculates network address, broadcast, host range, wildcard mask, and more
from CIDR notation or IP + subnet mask. Supports IPv4 and IPv6.
"""

import argparse
import ipaddress
import json
import sys
import textwrap


def calc_ipv4(network: ipaddress.IPv4Network) -> dict:
    """Calculate all IPv4 subnet details."""
    num_addresses = network.num_addresses
    num_hosts = max(0, num_addresses - 2) if network.prefixlen < 31 else num_addresses

    result = {
        "cidr": str(network),
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "subnet_mask": str(network.netmask),
        "wildcard_mask": str(network.hostmask),
        "prefix_length": network.prefixlen,
        "total_addresses": num_addresses,
        "usable_hosts": num_hosts,
        "is_private": network.is_private,
        "is_loopback": network.is_loopback,
        "is_multicast": network.is_multicast,
        "is_link_local": network.is_link_local,
    }

    if num_hosts > 0 and network.prefixlen < 31:
        hosts = list(network.hosts())
        result["first_host"] = str(hosts[0])
        result["last_host"] = str(hosts[-1])
    elif network.prefixlen == 31:
        # RFC 3021 point-to-point
        hosts = list(network)
        result["first_host"] = str(hosts[0])
        result["last_host"] = str(hosts[1])
    elif network.prefixlen == 32:
        result["first_host"] = str(network.network_address)
        result["last_host"] = str(network.network_address)

    # Binary representation
    net_int = int(network.network_address)
    result["binary_network"] = f"{net_int:032b}"
    mask_int = int(network.netmask)
    result["binary_mask"] = f"{mask_int:032b}"

    return result


def calc_ipv6(network: ipaddress.IPv6Network) -> dict:
    """Calculate IPv6 subnet details."""
    num_addresses = network.num_addresses

    result = {
        "cidr": str(network),
        "network_address": str(network.network_address),
        "prefix_length": network.prefixlen,
        "total_addresses": num_addresses,
        "is_private": network.is_private,
        "is_loopback": network.is_loopback,
        "is_multicast": network.is_multicast,
        "is_link_local": network.is_link_local,
        "compressed": str(network.network_address.compressed),
        "exploded": str(network.network_address.exploded),
    }

    if num_addresses > 2:
        hosts = network.hosts()
        first = next(hosts)
        result["first_host"] = str(first)
        # For large IPv6 ranges, compute last host directly
        last = network.broadcast_address - 1 if network.prefixlen < 127 else network.broadcast_address
        result["last_host"] = str(ipaddress.IPv6Address(last)) if isinstance(last, int) else str(last)

    return result


def check_contains(network, ip_str: str) -> dict:
    """Check if an IP address is within the network."""
    try:
        addr = ipaddress.ip_address(ip_str)
        return {
            "ip": str(addr),
            "network": str(network),
            "contained": addr in network,
        }
    except ValueError as e:
        return {"error": f"Invalid IP address: {e}"}


def split_subnet(network: ipaddress.IPv4Network, new_prefix: int) -> list[str]:
    """Split a network into smaller subnets."""
    if new_prefix <= network.prefixlen:
        print(f"Error: new prefix /{new_prefix} must be larger than /{network.prefixlen}", file=sys.stderr)
        sys.exit(1)
    if new_prefix > 32:
        print("Error: prefix cannot exceed /32", file=sys.stderr)
        sys.exit(1)
    return [str(subnet) for subnet in network.subnets(new_prefix=new_prefix)]


def format_plain(data: dict) -> str:
    """Format results as aligned plain text."""
    lines = []
    max_key = max(len(k) for k in data)
    for key, value in data.items():
        label = key.replace("_", " ").title()
        lines.append(f"  {label:<{max_key + 4}} {value}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="CIDR/Subnet calculator for IPv4 and IPv6 networks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s 192.168.1.0/24            # Calculate subnet details
              %(prog)s 10.0.0.0/8 -f json        # Output as JSON
              %(prog)s 172.16.0.0/16 --contains 172.16.5.10
              %(prog)s 192.168.0.0/22 --split 24  # Split into /24 subnets
              %(prog)s 2001:db8::/32              # IPv6 support
        """),
    )
    parser.add_argument("cidr", help="Network in CIDR notation (e.g. 192.168.1.0/24)")
    parser.add_argument(
        "-f", "--format", choices=["plain", "json"], default="plain",
        dest="fmt", help="Output format (default: plain)",
    )
    parser.add_argument(
        "--contains", metavar="IP",
        help="Check if an IP address is within the network",
    )
    parser.add_argument(
        "--split", type=int, metavar="PREFIX",
        help="Split network into subnets with this prefix length",
    )

    args = parser.parse_args()

    try:
        network = ipaddress.ip_network(args.cidr, strict=False)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Containment check
    if args.contains:
        result = check_contains(network, args.contains)
        if args.fmt == "json":
            print(json.dumps(result, indent=2))
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                status = "YES ✓" if result["contained"] else "NO ✗"
                print(f"  {result['ip']} in {result['network']}: {status}")
        return

    # Split operation
    if args.split is not None:
        if isinstance(network, ipaddress.IPv6Network):
            print("Error: --split currently supports IPv4 only", file=sys.stderr)
            sys.exit(1)
        subnets = split_subnet(network, args.split)
        if args.fmt == "json":
            print(json.dumps({"parent": str(network), "subnets": subnets}, indent=2))
        else:
            print(f"  Splitting {network} into /{args.split} subnets ({len(subnets)} total):\n")
            for s in subnets:
                print(f"    {s}")
        return

    # Standard calculation
    if isinstance(network, ipaddress.IPv6Network):
        data = calc_ipv6(network)
    else:
        data = calc_ipv4(network)

    if args.fmt == "json":
        print(json.dumps(data, indent=2))
    else:
        print(f"\n  Subnet Details for {args.cidr}\n  {'─' * 40}")
        print(format_plain(data))
        print()


if __name__ == "__main__":
    main()
