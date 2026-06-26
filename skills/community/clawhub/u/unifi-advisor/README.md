# OpenClaw UniFi Skill

A read-only [OpenClaw](https://openclaw.ai) skill that lets your AI assistant query your UniFi network and give advice on devices, clients, firewall configuration, VPN tunnels, ISP performance, and more — GET-only, no writes of any kind.

## What it does

Covers two official UniFi API surfaces:

**Site Manager API** (cloud, cross-site):
- Lists all consoles, sites, and devices on your UI account
- ISP performance metrics and SD-WAN configurations

**Network Integration API** (proxied via api.ui.com):
- Devices, clients, networks, WiFi SSIDs
- Firewall zones, policies, ACL rules, DNS policies
- VPN tunnels and servers, WAN interfaces
- Hotspot vouchers, RADIUS profiles, device tags
- DPI categories and applications

**All queries are GET-only. No writes, no mutations.**

## Structure

```
open_claw-unifi-skill/
├── SKILL.md           # Skill definition and agent instructions
└── scripts/
    └── unifi.py       # Query script
```

## Requirements

- A UI account at [unifi.ui.com](https://unifi.ui.com)
- Python 3 on the host running OpenClaw

## Setup

### 1. Generate an API key

Sign in at [unifi.ui.com](https://unifi.ui.com) → **Settings → API Keys** → create a new key.
The same key works for both the Site Manager and Network Integration APIs.

### 2. Set the API key on your OpenClaw host

```bash
export UNIFI_API_KEY=your-api-key-here
```

That's it. Host and site IDs are discovered automatically from your UI account on every invocation (cached for 15 minutes). No other env vars needed.

### 3. Install the skill

```bash
# From ClawHub (once published):
openclaw skills install unifi-advisor

# Or locally:
openclaw skills install /path/to/open_claw-unifi-skill
```

## Usage

Ask your assistant naturally:

- *"Are all my UniFi devices online?"*
- *"Which clients are connected right now?"*
- *"Show me my firewall policies and check for anything too broad"*
- *"Is my VPN tunnel up?"*
- *"How is my ISP performing?"*
- *"What networks and VLANs do I have configured?"*

If you have multiple sites, specify which one: *"Check the firewall on my HQ site"* or *"What clients are on the branch office network?"*

Or call directly for testing:

```bash
python3 scripts/unifi.py list                         # all available subcommands
python3 scripts/unifi.py library                      # show discovered sites
python3 scripts/unifi.py devices --site hq            # adopted devices on a specific site
python3 scripts/unifi.py clients --limit 20           # connected clients
python3 scripts/unifi.py firewall-policies            # firewall policies
python3 scripts/unifi.py isp-metrics --metric-type 1h # ISP performance
```

## All subcommands

### Site Manager (cloud)

| Subcommand | Description |
|---|---|
| `library` | Show discovered sites with labels, state, and API capabilities |
| `hosts` | All UniFi OS consoles on the UI account |
| `host` | Console details (`--id` required) |
| `sites` | All sites across all consoles |
| `cloud-devices` | All devices across all sites |
| `isp-metrics` | ISP performance metrics (`--metric-type 1h\|5m`) |
| `sdwan` | SD-WAN configurations |
| `sdwan-config` | SD-WAN config details (`--id` required) |
| `sdwan-status` | SD-WAN deployment status (`--id` required) |

### Network Integration (per-site, use `--site <label>`)

| Subcommand | Description |
|---|---|
| `info` | Controller version and capabilities |
| `net-sites` | Sites managed by this console |
| `devices` | Adopted devices overview |
| `device` | Device details (`--id` required) |
| `device-stats` | Latest device statistics (`--id` required) |
| `devices-pending` | Devices pending adoption |
| `clients` | Connected clients overview |
| `client` | Client details (`--id` required) |
| `networks` | Networks overview |
| `network` | Network details (`--id` required) |
| `network-refs` | References to a network — devices, clients, WiFi (`--id` required; use a network with active traffic) |
| `wifi` | WiFi broadcast (SSID) overview |
| `wifi-details` | WiFi broadcast details (`--id` required) |
| `firewall-zones` | Firewall zones |
| `firewall-zone` | Firewall zone details (`--id` required) |
| `firewall-policies` | Firewall policies |
| `firewall-policy` | Firewall policy details (`--id` required) |
| `firewall-ordering` | Firewall policy ordering between two zones (`--from-zone` and `--to-zone` required) |
| `acl-rules` | ACL rules |
| `acl-rule` | ACL rule details (`--id` required) |
| `acl-ordering` | ACL rule ordering |
| `dns-policies` | DNS policies |
| `dns-policy` | DNS policy details (`--id` required) |
| `traffic-lists` | Traffic matching lists |
| `traffic-list` | Traffic matching list details (`--id` required) |
| `vouchers` | Hotspot vouchers |
| `voucher` | Voucher details (`--id` required) |
| `wans` | WAN interfaces overview |
| `vpn-tunnels` | Site-to-site VPN tunnels |
| `vpn-servers` | VPN server configurations |
| `radius` | RADIUS profiles |
| `device-tags` | Device tags |
| `dpi-categories` | DPI application categories |
| `dpi-applications` | DPI applications |
| `countries` | Countries list (for geo-IP firewall rules) |

## License

MIT-0 — do whatever you want with it, no attribution required.
