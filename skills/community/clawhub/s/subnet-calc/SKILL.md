---
name: subnet-calc
description: CIDR and subnet calculator for network engineers. Calculate network address, broadcast, host range, subnet mask, wildcard mask, and more from CIDR notation. Supports IPv4 and IPv6, containment checks, and subnet splitting. Use when working with IP addresses, subnets, network planning, CIDR calculations, or checking if an IP is within a range.
---

# Subnet Calc

CIDR/subnet calculator CLI. IPv4 and IPv6 support with no external dependencies.

## Quick Start

```bash
# Basic subnet calculation
python3 scripts/subnet_calc.py 192.168.1.0/24

# JSON output
python3 scripts/subnet_calc.py 10.0.0.0/8 -f json

# Check if IP is in a network
python3 scripts/subnet_calc.py 172.16.0.0/16 --contains 172.16.5.10

# Split into smaller subnets
python3 scripts/subnet_calc.py 192.168.0.0/22 --split 24

# IPv6
python3 scripts/subnet_calc.py 2001:db8::/32
```

## Output Fields (IPv4)

- **CIDR** — Normalized CIDR notation
- **Network/Broadcast Address** — First and last address in the range
- **Subnet Mask / Wildcard Mask** — Standard and inverted masks
- **Total Addresses / Usable Hosts** — Address count minus network and broadcast
- **First/Last Host** — Usable host range
- **Binary representations** — Network and mask in binary
- **Flags** — Private, loopback, multicast, link-local detection

## Options

| Flag | Description |
|------|-------------|
| `-f, --format` | `plain` or `json` output |
| `--contains IP` | Check if IP is within the network |
| `--split PREFIX` | Split into subnets with given prefix (IPv4) |

## Notes

- Python 3 stdlib only (uses `ipaddress` module)
- Handles /31 (RFC 3021 point-to-point) and /32 correctly
- Input is normalized with `strict=False` (host bits are masked)
