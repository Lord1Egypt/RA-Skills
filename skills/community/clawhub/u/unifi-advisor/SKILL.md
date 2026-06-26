---
name: unifi-advisor
description: Read-only UniFi network advisor covering the Site Manager cloud API and the Network Integration API. Query devices, clients, networks, firewall zones and policies, ACL rules, DNS policies, VPN tunnels, DPI, ISP metrics, and related UniFi state. Use when inspecting UniFi environments with GET-only operations and no writes.
metadata: {"openclaw":{"requires":{"env":["UNIFI_API_KEY"],"bins":["python3"]},"primaryEnv":"UNIFI_API_KEY"}}
---

# UniFi Network Advisor

Read-only skill covering two official UniFi API surfaces. All operations are GET-only — no writes, no mutations of any kind.

## API surfaces

Everything goes through `https://api.ui.com`. No direct local connection required.

| Prefix | Surface | Proxied via | Env vars needed |
|---|---|---|---|
| SM | Site Manager | `api.ui.com/v1/...` | `UNIFI_API_KEY` |
| NET | Network Integration | `api.ui.com/v1/connector/consoles/{hostId}/proxy/network/integration/v1/...` | `UNIFI_API_KEY` (host/site resolved automatically) |

## How to call the script

```
python3 {baseDir}/scripts/unifi.py <subcommand> [--site SITE] [--id ID] [--limit N] [--next-token TOKEN] [subcommand-specific flags]
```

Some subcommands require additional flags — see the table below. Use `python3 {baseDir}/scripts/unifi.py list` to see all subcommands with descriptions.

## Subcommands

### Site Manager (SM) — cloud, single API key

| Subcommand | Endpoint | Required flags | Description |
|---|---|---|---|
| `hosts` | GET /v1/hosts | — | All UniFi OS consoles on the UI account |
| `host` | GET /v1/hosts/{id} | `--id` | Console details |
| `sites` | GET /v1/sites | — | All sites across all consoles |
| `cloud-devices` | GET /v1/devices | — | All devices across all sites |
| `isp-metrics` | GET /ea/isp-metrics/{type} | — | ISP performance metrics |
| `sdwan` | GET /v1/sd-wan-configs | — | SD-WAN configurations |
| `sdwan-config` | GET /v1/sd-wan-configs/{id} | `--id` | Specific SD-WAN config |
| `sdwan-status` | GET /v1/sd-wan-configs/{id}/status | `--id` | SD-WAN deployment status |

### Network Integration (NET) — proxied via api.ui.com, site resolved automatically

| Subcommand | Endpoint | Required flags | Description |
|---|---|---|---|
| `info` | GET /v1/info | — | Controller version and capabilities |
| `net-sites` | GET /v1/sites | — | Sites managed by this console |
| `devices` | GET /v1/sites/{siteId}/devices | — | Adopted devices overview |
| `device` | GET /v1/sites/{siteId}/devices/{id} | `--id` | Device details |
| `device-stats` | GET /v1/sites/{siteId}/devices/{id}/statistics/latest | `--id` | Latest device statistics |
| `devices-pending` | GET /v1/pending-devices | — | Devices pending adoption (console-scoped) |
| `clients` | GET /v1/sites/{siteId}/clients | — | Connected clients overview |
| `client` | GET /v1/sites/{siteId}/clients/{id} | `--id` | Client details |
| `networks` | GET /v1/sites/{siteId}/networks | — | Networks overview |
| `network` | GET /v1/sites/{siteId}/networks/{id} | `--id` | Network details |
| `network-refs` | GET /v1/sites/{siteId}/networks/{id}/references | `--id` | What references a specific network (devices, clients, WiFi) |
| `wifi` | GET /v1/sites/{siteId}/wifi/broadcasts | — | WiFi broadcast (SSID) overview |
| `wifi-details` | GET /v1/sites/{siteId}/wifi/broadcasts/{id} | `--id` | WiFi broadcast details |
| `firewall-zones` | GET /v1/sites/{siteId}/firewall/zones | — | Firewall zones |
| `firewall-zone` | GET /v1/sites/{siteId}/firewall/zones/{id} | `--id` | Firewall zone details |
| `firewall-policies` | GET /v1/sites/{siteId}/firewall/policies | — | Firewall policies |
| `firewall-policy` | GET /v1/sites/{siteId}/firewall/policies/{id} | `--id` | Firewall policy details |
| `firewall-ordering` | GET /v1/sites/{siteId}/firewall/policies/ordering | `--from-zone` `--to-zone` | Policy ordering between two zones |
| `acl-rules` | GET /v1/sites/{siteId}/acl-rules | — | ACL rules |
| `acl-rule` | GET /v1/sites/{siteId}/acl-rules/{id} | `--id` | ACL rule details |
| `acl-ordering` | GET /v1/sites/{siteId}/acl-rules/ordering | — | ACL rule ordering |
| `dns-policies` | GET /v1/sites/{siteId}/dns/policies | — | DNS policies |
| `dns-policy` | GET /v1/sites/{siteId}/dns/policies/{id} | `--id` | DNS policy details |
| `traffic-lists` | GET /v1/sites/{siteId}/traffic-matching-lists | — | Traffic matching lists |
| `traffic-list` | GET /v1/sites/{siteId}/traffic-matching-lists/{id} | `--id` | Traffic matching list details |
| `vouchers` | GET /v1/sites/{siteId}/hotspot/vouchers | — | Hotspot vouchers |
| `voucher` | GET /v1/sites/{siteId}/hotspot/vouchers/{id} | `--id` | Voucher details |
| `wans` | GET /v1/sites/{siteId}/wans | — | WAN interfaces overview |
| `vpn-tunnels` | GET /v1/sites/{siteId}/vpn/site-to-site-tunnels | — | Site-to-site VPN tunnels |
| `vpn-servers` | GET /v1/sites/{siteId}/vpn/servers | — | VPN server configurations |
| `radius` | GET /v1/sites/{siteId}/radius/profiles | — | RADIUS profiles |
| `device-tags` | GET /v1/sites/{siteId}/device-tags | — | Device tags |
| `dpi-categories` | GET /v1/dpi/categories | — | DPI application categories |
| `dpi-applications` | GET /v1/dpi/applications | — | DPI applications |
| `countries` | GET /v1/countries | — | Countries list (for geo-IP rules) |

## Examples

```bash
# List all sites and pick one to work with
python3 {baseDir}/scripts/unifi.py library

# firewall-ordering: get zone IDs first, then query ordering between two of them
# --from-zone and --to-zone must be real UUIDs from the firewall-zones output
python3 {baseDir}/scripts/unifi.py firewall-zones --site hq
python3 {baseDir}/scripts/unifi.py firewall-ordering --site hq --from-zone <zoneId> --to-zone <zoneId>

# network-refs: get network list first, then query references for a specific network
python3 {baseDir}/scripts/unifi.py networks --site hq
python3 {baseDir}/scripts/unifi.py network-refs --site hq --id <networkId>

# sdwan-config / sdwan-status: list configs first to get an ID
python3 {baseDir}/scripts/unifi.py sdwan
python3 {baseDir}/scripts/unifi.py sdwan-config --id <configId>
python3 {baseDir}/scripts/unifi.py sdwan-status --id <configId>
```

## Site library

On every invocation the skill builds a site library by joining:
- `GET /v1/hosts` — host names (user-set), hardware model, connection state, `apiIntegration` flag
- `GET /v1/sites` — `siteId` per `hostId`

Labels come directly from the name the user set in the UniFi UI — e.g. "HQ" → `hq`, "Branch Office" → `branch-office`, "Remote Site" → `remote-site`. The library is cached in `~/.openclaw/unifi-skill.json` for 15 minutes to avoid redundant API calls.

Hosts without Network API support (e.g. a NAS device with `apiIntegration: false`) are included in the library but will return a clear error if targeted with NET subcommands.

Run `library` to see the current library including state, hardware, and API capability of each host.

## Site selection

All NET subcommands accept `--site <hint>`. The hint is matched against label, name, hardware shortname, hardware name, timezone, and IP — partial matches work.

| User says | Use |
|---|---|
| "the main office network" | `--site hq` |
| "remote site firewall" | `--site remote-site` |
| "the branch office" | `--site branch-office` |
| "the Dream Machine Pro" | `--site udmpro` |
| "the warehouse AP" | `--site warehouse` |

If `--site` is omitted the first entry in the library is used. If the hint is ambiguous the skill lists the matching labels and asks for a more specific hint.

**Always specify `--site` when the user mentions a location or device.** When the user says "my network" without specifying, run `library` first to show what sites are available and ask which one they mean.

## How to give advice

### Devices (`devices`, `device`)
- `status != "online"` → offline or disconnected — surface to user
- `firmwareStatus: "updateAvailable"` → firmware update pending
- `device-stats` → CPU/memory/uptime signals for performance issues

### Clients (`clients`, `client`)
- High noise or weak signal → coverage gap, suggest AP placement review
- Unexpected clients on sensitive VLANs → flag for review

### Firewall (`firewall-policies`, `firewall-zones`, `acl-rules`)
- Policies allowing all traffic between sensitive zones → flag as overly broad
- Cross-zone allow rules → confirm intentional with user
- Check `firewall-ordering` — rules are evaluated in order; misplaced rules cause unexpected behaviour

### DNS (`dns-policies`)
- Custom DNS policies can bypass filtering — flag any unexpected overrides

### VPN (`vpn-tunnels`, `vpn-servers`)
- Tunnel state down → connectivity issue to surface
- Verify expected peers are configured

### ISP metrics (`isp-metrics`)
- Packet loss > 1% or latency spikes → WAN quality issue, advise checking with ISP

## Notes

- `network-refs` requires `--id` (a network ID). Only networks with active references (devices, clients, or WiFi assigned to them) return data — unused networks return a handled error: `"Network '...' has no active references"`. Run `networks` first to list all networks, then pass the ID of one that carries traffic.
- `firewall-ordering` requires both `--from-zone` and `--to-zone`. Run `firewall-zones` first to list zone IDs. The API returns the ordered policy IDs for traffic flowing from the source zone to the destination zone.
- `sdwan-config` and `sdwan-status` require `--id`. Run `sdwan` first to list configs and get an ID. These return empty on accounts without SD-WAN configured.

## Source & contributing

Source code, issue tracker, and contributions: [github.com/arseni-mik/open_claw-unifi-skill](https://github.com/arseni-mik/open_claw-unifi-skill/tree/main)

## Constraints

- All operations are GET-only. Never suggest using this skill to make changes.
- Guide the user to make changes in the UniFi dashboard or mobile app.
- Do not expose raw API keys in responses.
