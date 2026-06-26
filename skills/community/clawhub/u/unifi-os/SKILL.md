# UniFi Network Skill

Read-only access to UniFi Network data for infrastructure documentation and troubleshooting. Covers devices, networks, clients, health, alerts, and topology export.

**Base URL:** configured via `UNIFI_URL` (e.g. `https://UniFi.Url.Here.local`)
**Auth:** API key via `X-API-Key` header — no session management
**Site:** `default` unless overridden via `UNIFI_SITE`

## API Response Shape

The UniFi OS (UOS) API has two response formats:

- **v2 device endpoint** (`/proxy/network/v2/api/site/{site}/device`): returns `{"network_devices": [...], "unmanaged_devices": [...]}` — NOT `{"data": [...]}`. All device scripts account for this.
- **Legacy endpoints** (`/proxy/network/api/s/{site}/...`): return `{"data": [...]}`. Used by health, clients, networks, wlans, alerts, dpi, ports.

WAN subsystem health returns `"unknown"` status when no UniFi gateway is adopted (e.g. TNSR/other router). LAN status shows `"error"` when `num_disconnected > 0`.

## Setup

Create `~/.clawdbot/credentials/unifi/config.json`:
```json
{
  "url": "https://UniFi.Url.Here.local",
  "api_key": "YOUR_API_KEY",
  "site": "default"
}
```
`chmod 600 ~/.clawdbot/credentials/unifi/config.json`

API key: UniFi OS → Settings → System → API → Create API Key (read-only scopes).

Or use env vars: `UNIFI_URL`, `UNIFI_API_KEY`, `UNIFI_SITE`.

## Token & API Efficiency Rules

**Always follow these — they exist to minimize API calls and token use:**

1. **Call `snapshot.sh` first** before any other script. Read its output. Only proceed to specific scripts if the answer isn't already there.
2. **Rely on cache.** Scripts cache responses and serve from disk when fresh. Do not force re-runs to get "fresher" data unless debugging.
3. **Use `client_locate.sh` for any device/client lookup.** It joins clients + devices + networks in one call. Never call those three scripts separately for the same query.
4. **Use stripped output (default).** Only use `--json` or `--raw` if you need fields not present in the default output.
5. **Don't call scripts you don't need.** If `snapshot.sh` shows 0 open alerts, skip `alerts.sh`.

## Cache TTLs

| Data | TTL | Scripts |
|------|-----|---------|
| Inventory | 60 min | devices, networks, wlans, port_profiles, port_forwards |
| Operational | 5 min | health, clients, dpi |
| Alerts | 60 sec | alerts |

Cache lives at `~/.clawdbot/cache/unifi/`. Each script prints cache age in its header.

## Scripts

### snapshot.sh [--json]
**Start here.** Compact overview: WAN status, device/client/network/alert counts, device health list, VLAN list, top open alerts.

Trigger when: user asks general "how's the network", "UniFi status", "what's connected", "any issues".

```bash
bash scripts/snapshot.sh
```

---

### devices.sh [--json] [--raw]
All adopted devices: name, model, IP, status, client count, firmware.

Trigger when: "list all devices", "show APs", "what switches do I have", "device inventory".

```bash
bash scripts/devices.sh
```

---

### networks.sh [--json] [--raw]
All network configs: name, purpose, VLAN ID, subnet, DHCP state.

Trigger when: "what VLANs exist", "show network config", "what subnet is X on", "DHCP ranges".

```bash
bash scripts/networks.sh
```

---

### wlans.sh [--json] [--raw]
Wireless networks: SSID, security, VLAN, enabled state, hidden.

Trigger when: "what SSIDs are configured", "wireless networks", "what VLAN is SSID X on".

```bash
bash scripts/wlans.sh
```

---

### port_profiles.sh [--json] [--raw]
Switch port profiles: name, native VLAN, PoE mode, speed.

Trigger when: "what port profiles exist", "how is port profile X configured", "PoE profiles".

```bash
bash scripts/port_profiles.sh
```

---

### port_forwards.sh [--json] [--raw]
NAT/port forward rules: name, proto, external port, internal dest, state.

Trigger when: "what ports are forwarded", "port forwarding rules", "is port X forwarded", "NAT rules".

```bash
bash scripts/port_forwards.sh
```

---

### firmware.sh [--json] [--all]
Devices with pending firmware updates. Default: only shows devices needing update. `--all`: shows all with current version.

Trigger when: "firmware updates", "what needs upgrading", "firmware versions", change management docs.

```bash
bash scripts/firmware.sh
bash scripts/firmware.sh --all  # full version inventory
```

---

### health.sh [--json] [--raw]
Subsystem health: WAN, LAN, WLAN status and counters.

Trigger when: "is WAN up", "network health", "any subsystem issues".

```bash
bash scripts/health.sh
```

---

### alerts.sh [N] [--json] [--archived]
Recent open alarms. Default: 20, unarchived.

Trigger when: "any alerts", "recent alarms", "what went wrong", incident investigation.

```bash
bash scripts/alerts.sh
bash scripts/alerts.sh 50 --archived
```

---

### clients.sh [--json] [--raw] [--wifi|--wired]
All active connected clients: hostname, IP, VLAN, AP or switch+port.

Trigger when: "who's connected", "active clients", "how many devices on the network".
**Not for locating a specific client — use `client_locate.sh` instead.**

```bash
bash scripts/clients.sh
bash scripts/clients.sh --wired
```

---

### client_history.sh [hours] [--json]
Clients seen in last N hours, including disconnected. Default: 24h.

Trigger when: "did X connect today", "recently disconnected devices", "was Y on the network".

```bash
bash scripts/client_history.sh
bash scripts/client_history.sh 48
```

---

### dpi.sh [N] [--json]
Top N apps by bandwidth via DPI. Default: 10.

Trigger when: "what's using bandwidth", "top applications", "bandwidth hogs".

```bash
bash scripts/dpi.sh
bash scripts/dpi.sh 20
```

---

### device_detail.sh <name|ip|mac> [--json]
Full detail on one device: all ports with speed/PoE/errors, radio table, firmware update status.

Trigger when: troubleshooting a specific switch or AP — "is port 5 on SW-Core up", "what channel is AP-Living on", "PoE draw on the living room switch".

```bash
bash scripts/device_detail.sh AP-Living
bash scripts/device_detail.sh 10.0.5.12
bash scripts/device_detail.sh dc:a6:32:xx:xx:xx
```

---

### client_locate.sh <name|ip|mac> [--json] [--include-history]
**Most useful troubleshooting tool.** Finds a client and returns: IP, MAC, VLAN, network name, AP or switch+port, signal (if WiFi), last seen. Joins clients+devices+networks from cache — one output, no chaining.

Add `--include-history` to find recently disconnected clients.

Trigger when: "where is device X", "what port is printer Y on", "what VLAN is Z on", "find hostname X", "I can't reach device X".

```bash
bash scripts/client_locate.sh "MacBook"
bash scripts/client_locate.sh 192.0.10.55
bash scripts/client_locate.sh --include-history "old-laptop"
```

---

### topology_export.sh [--out <file>]
Full site topology as markdown: devices table, VLANs table, WLANs table, port forwards. Designed for BookStack, memory writes, or documentation.

Trigger when: "generate network documentation", "export topology", "write to memory", "document the network".

```bash
bash scripts/topology_export.sh
bash scripts/topology_export.sh --out ~/clawd/memory/bank/unifi-topology.md
```

---

## Workflow Examples

**"Is the network healthy?"**
→ `snapshot.sh` only. Done.

**"Where is the NAS?"**
→ `client_locate.sh NAS` only. Done.

**"What's eating all the bandwidth?"**
→ `snapshot.sh` (confirms WAN up), then `dpi.sh`. Two scripts.

**"Document the network for BookStack"**
→ `topology_export.sh --out <path>`. One script.

**"AP-Living seems slow"**
→ `device_detail.sh AP-Living`. One script. Check channel, clients, signal.

**"I can't reach 172.0.20.5"**
→ `client_locate.sh 172.0.20.5`. If not found: `client_locate.sh --include-history 172.0.20.5`. Then `health.sh` if VLAN issue suspected.
