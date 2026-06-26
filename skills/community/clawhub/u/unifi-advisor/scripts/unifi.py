#!/usr/bin/env python3
"""
UniFi read-only skill for OpenClaw.

All requests go through https://api.ui.com — no direct local connection required.
Network Integration endpoints are proxied via:
  https://api.ui.com/v1/connector/consoles/{hostId}/proxy/network/integration/v1/...

The site library is built automatically on every invocation by joining:
  GET /api/v1/hosts  → host names, hardware, connection state, apiIntegration flag
  GET /api/v1/sites  → siteId per hostId

Library labels come from the user-set host name (e.g. "Home", "Office").
The library is cached for 15 minutes to avoid redundant API calls.

Required env var:
  UNIFI_API_KEY  — API key from unifi.ui.com → Settings → API Keys
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────────

API_KEY          = os.environ.get("UNIFI_API_KEY", "")
SM_BASE          = "https://api.ui.com"
CACHE_FILE       = Path.home() / ".openclaw" / "unifi-skill.json"
CACHE_TTL        = 900  # 15 minutes


# ── HTTP ─────────────────────────────────────────────────────────────────────────

def _err(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


def _get(url: str, params: dict | None = None) -> dict | list:
    if not API_KEY:
        _err("UNIFI_API_KEY is not set — generate one at unifi.ui.com → Settings → API Keys")
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"X-API-Key": API_KEY, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode())
            return body.get("data", body)
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        _err(f"HTTP {e.code}: {e.reason} — {body[:200]}")
    except urllib.error.URLError as e:
        _err(f"Cannot reach {url}: {e.reason}")


def _sm(path: str, params: dict | None = None):
    return _get(f"{SM_BASE}/{path}", params)


def _net(path: str, entry: dict, params: dict | None = None):
    if not entry.get("apiIntegration"):
        _err(
            f"Host '{entry['name']}' ({entry['shortname']}) does not support the "
            "Network Integration API (apiIntegration=false)"
        )
    if not entry.get("hasNetwork"):
        _err(
            f"Host '{entry['name']}' ({entry['shortname']}) has no running Network "
            "controller — Network API subcommands are not available for this host"
        )
    return _get(
        f"{SM_BASE}/v1/connector/consoles/{entry['hostId']}/proxy/network/integration/v1/{path}",
        params,
    )


# ── Site library ─────────────────────────────────────────────────────────────────

def _build_label(name: str) -> str:
    return name.lower().strip().replace(" ", "-")


def _load_library() -> list:
    """Return cached library if fresh, otherwise refresh from API."""
    if CACHE_FILE.exists():
        try:
            cached = json.loads(CACHE_FILE.read_text())
            if time.time() - cached.get("updatedAt", 0) < CACHE_TTL and cached.get("library"):
                return cached["library"]
        except Exception:
            pass
    return _refresh_library()


def _net_raw(path: str, host_id: str, params: dict | None = None):
    """Direct Network Integration API call using only a hostId — used during library build."""
    return _get(
        f"{SM_BASE}/v1/connector/consoles/{host_id}/proxy/network/integration/v1/{path}",
        params,
    )


def _refresh_library() -> list:
    """
    Fetch hosts from the Site Manager, then for each network-capable host fetch
    the site ID from the Network Integration API (its own /v1/sites). The two APIs
    use different site ID formats — only the Network Integration API's own ID works
    for site-scoped calls like /v1/sites/{siteId}/clients.
    """
    hosts_raw = _sm("v1/hosts") or []
    if isinstance(hosts_raw, dict):
        hosts_raw = [hosts_raw]

    library = []
    seen_labels: dict[str, int] = {}

    for h in hosts_raw:
        host_id = h.get("id", "")
        rs      = h.get("reportedState", {})
        name    = (rs.get("name") or "").strip() or host_id
        label   = _build_label(name)

        if label in seen_labels:
            seen_labels[label] += 1
            label = f"{label}-{seen_labels[label]}"
        else:
            seen_labels[label] = 0

        hw          = rs.get("hardware", {})
        features    = rs.get("features", {})
        has_api     = features.get("apiIntegration", False)
        has_network = any(
            c.get("name") == "network" and c.get("isRunning", False)
            for c in rs.get("controllers", [])
        )

        # Get the siteId from the Network Integration API — NOT from the Site Manager.
        # The two use different ID formats; only the NET API's own ID works for
        # site-scoped calls like /v1/sites/{siteId}/clients.
        site_id = ""
        if has_api and has_network:
            try:
                net_sites = _net_raw("sites", host_id) or []
                if isinstance(net_sites, dict):
                    net_sites = [net_sites]
                if net_sites:
                    site_id = net_sites[0].get("id") or net_sites[0].get("siteId", "")
            except SystemExit:
                pass  # host unreachable — leave site_id empty

        library.append({
            "label":          label,
            "name":           name,
            "hostId":         host_id,
            "siteId":         site_id,
            "hardware":       hw.get("name", ""),
            "shortname":      hw.get("shortname", ""),
            "firmwareVersion": hw.get("firmwareVersion", ""),
            "state":          rs.get("state", ""),
            "apiIntegration": has_api,
            "hasNetwork":     has_network,
            "timezone":       rs.get("timezone", ""),
            "ip":             rs.get("ip", ""),
        })

    CACHE_FILE.write_text(json.dumps({"library": library, "updatedAt": time.time()}, indent=2))
    return library


def _resolve(library: list, hint: str | None) -> dict:
    """
    Find a library entry by label or partial match against name, shortname,
    hardware name, timezone, or IP. Defaults to first entry if no hint given.
    """
    if not hint:
        return library[0]

    h = hint.lower()

    # Exact label match
    for e in library:
        if e["label"] == h:
            return e

    # Partial match across useful fields
    matches = [
        e for e in library
        if h in e["label"]
        or h in e["name"].lower()
        or h in e["shortname"].lower()
        or h in e["hardware"].lower()
        or h in e["timezone"].lower()
        or h in e["ip"]
    ]

    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        _err(
            f"Ambiguous site hint '{hint}' matches: "
            + ", ".join(m["label"] for m in matches)
            + " — be more specific"
        )
    _err(
        f"No site matching '{hint}'. Available: "
        + ", ".join(e["label"] for e in library)
    )


def _ctx(a) -> dict:
    return _resolve(_load_library(), getattr(a, "site", None))


# ── Shared helpers ───────────────────────────────────────────────────────────────

def _require_id(a) -> str:
    if not a.id:
        _err("--id is required for this subcommand")
    return a.id


def _page(a) -> dict | None:
    p = {k: v for k, v in {"pageSize": a.limit, "nextToken": a.next_token}.items() if v is not None}
    return p or None


def _out(data, limit: int | None = None) -> None:
    if limit and isinstance(data, list):
        data = data[:limit]
    print(json.dumps(data, indent=2))


# ── Library subcommands ──────────────────────────────────────────────────────────

def cmd_library(a):
    """Show the current site library (refreshes if cache is stale)."""
    lib = _load_library()
    rows = [{
        "label":          e["label"],
        "name":           e["name"],
        "hardware":       e["hardware"],
        "shortname":      e["shortname"],
        "state":          e["state"],
        "apiIntegration": e["apiIntegration"],
        "hasNetwork":     e["hasNetwork"],
        "ip":             e["ip"],
        "timezone":       e["timezone"],
    } for e in lib]
    print(json.dumps(rows, indent=2))


# ── Site Manager API ─────────────────────────────────────────────────────────────

def sm_hosts(a):
    _out(_sm("v1/hosts", _page(a)))

def sm_host(a):
    _out(_sm(f"v1/hosts/{_require_id(a)}"))

def sm_sites(a):
    _out(_sm("v1/sites"), a.limit)

def sm_devices(a):
    _out(_sm("v1/devices"), a.limit)

def sm_isp_metrics(a):
    t = a.metric_type or "1h"
    if t not in ("1h", "5m"):
        _err("--metric-type must be '1h' or '5m'")
    params = {k: v for k, v in {
        "beginTimestamp": a.begin, "endTimestamp": a.end, "duration": a.duration
    }.items() if v}
    _out(_sm(f"ea/isp-metrics/{t}", params or None))

def sm_sdwan(a):
    _out(_sm("v1/sd-wan-configs"))

def sm_sdwan_config(a):
    _out(_sm(f"v1/sd-wan-configs/{_require_id(a)}"))

def sm_sdwan_status(a):
    _out(_sm(f"v1/sd-wan-configs/{_require_id(a)}/status"))


# ── Network Integration API ──────────────────────────────────────────────────────

def net_info(a):
    s = _ctx(a); _out(_net("info", s))

def net_net_sites(a):
    s = _ctx(a); _out(_net("sites", s), a.limit)

def net_devices(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/devices", s, _page(a)), a.limit)

def net_device(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/devices/{_require_id(a)}", s))

def net_device_stats(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/devices/{_require_id(a)}/statistics/latest", s))

def net_devices_pending(a):
    s = _ctx(a); _out(_net("pending-devices", s, _page(a)))

def net_clients(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/clients", s, _page(a)), a.limit)

def net_client(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/clients/{_require_id(a)}", s))

def net_networks(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/networks", s, _page(a)))

def net_network(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/networks/{_require_id(a)}", s))

def net_network_refs(a):
    s = _ctx(a)
    nid = _require_id(a)
    url = f"{SM_BASE}/v1/connector/consoles/{s['hostId']}/proxy/network/integration/v1/sites/{s['siteId']}/networks/{nid}/references"
    req = urllib.request.Request(url, headers={"X-API-Key": API_KEY, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode())
            _out(body.get("data", body))
    except urllib.error.HTTPError as e:
        if e.code == 500:
            _err(
                f"Network '{nid}' has no active references — the UniFi API returns 500 for networks "
                "with no devices, clients, or WiFi assigned to them. "
                "Run 'networks' to list all networks and pass the ID of one that carries traffic."
            )
        _err(f"HTTP {e.code}: {e.reason} — {(e.read().decode() if e.fp else '')[:200]}")
    except urllib.error.URLError as e:
        _err(f"Cannot reach {url}: {e.reason}")

def net_wifi(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/wifi/broadcasts", s, _page(a)))

def net_wifi_details(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/wifi/broadcasts/{_require_id(a)}", s))

def net_fw_zones(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/firewall/zones", s, _page(a)))

def net_fw_zone(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/firewall/zones/{_require_id(a)}", s))

def net_fw_policies(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/firewall/policies", s, _page(a)))

def net_fw_policy(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/firewall/policies/{_require_id(a)}", s))

def net_fw_ordering(a):
    if not a.from_zone or not a.to_zone:
        _err("firewall-ordering requires --from-zone <sourceZoneId> and --to-zone <destZoneId> — run firewall-zones to list zone IDs")
    s = _ctx(a)
    params = {"sourceFirewallZoneId": a.from_zone, "destinationFirewallZoneId": a.to_zone}
    _out(_net(f"sites/{s['siteId']}/firewall/policies/ordering", s, params))

def net_acl_rules(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/acl-rules", s, _page(a)))

def net_acl_rule(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/acl-rules/{_require_id(a)}", s))

def net_acl_ordering(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/acl-rules/ordering", s))

def net_dns_policies(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/dns/policies", s, _page(a)))

def net_dns_policy(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/dns/policies/{_require_id(a)}", s))

def net_traffic_lists(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/traffic-matching-lists", s, _page(a)))

def net_traffic_list(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/traffic-matching-lists/{_require_id(a)}", s))

def net_vouchers(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/hotspot/vouchers", s, _page(a)))

def net_voucher(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/hotspot/vouchers/{_require_id(a)}", s))

def net_wans(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/wans", s, _page(a)))

def net_vpn_tunnels(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/vpn/site-to-site-tunnels", s, _page(a)))

def net_vpn_servers(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/vpn/servers", s, _page(a)))

def net_radius(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/radius/profiles", s, _page(a)))

def net_device_tags(a):
    s = _ctx(a); _out(_net(f"sites/{s['siteId']}/device-tags", s, _page(a)))

def net_dpi_cats(a):
    s = _ctx(a); _out(_net("dpi/categories", s))

def net_dpi_apps(a):
    s = _ctx(a); _out(_net("dpi/applications", s, _page(a)))

def net_countries(a):
    s = _ctx(a); _out(_net("countries", s))


# ── Command registry ────────────────────────────────────────────────────────────

COMMANDS = {
    # Library
    "library":            (cmd_library,        "Show site library with labels, state, and API capabilities"),
    # Site Manager
    "hosts":              (sm_hosts,           "SM  · All UniFi OS consoles on the UI account"),
    "host":               (sm_host,            "SM  · Console details (--id required)"),
    "sites":              (sm_sites,           "SM  · Raw site list from Site Manager"),
    "cloud-devices":      (sm_devices,         "SM  · All devices across all sites"),
    "isp-metrics":        (sm_isp_metrics,     "SM  · ISP performance metrics (--metric-type 1h|5m) [EA]"),
    "sdwan":              (sm_sdwan,           "SM  · SD-WAN configurations [EA]"),
    "sdwan-config":       (sm_sdwan_config,    "SM  · SD-WAN config details (--id required) [EA]"),
    "sdwan-status":       (sm_sdwan_status,    "SM  · SD-WAN deployment status (--id required) [EA]"),
    # Network Integration
    "info":               (net_info,           "NET · Controller version and capabilities"),
    "net-sites":          (net_net_sites,      "NET · Sites on this console"),
    "devices":            (net_devices,        "NET · Adopted devices overview"),
    "device":             (net_device,         "NET · Device details (--id required)"),
    "device-stats":       (net_device_stats,   "NET · Latest device statistics (--id required)"),
    "devices-pending":    (net_devices_pending,"NET · Devices pending adoption"),
    "clients":            (net_clients,        "NET · Connected clients overview"),
    "client":             (net_client,         "NET · Client details (--id required)"),
    "networks":           (net_networks,       "NET · Networks overview"),
    "network":            (net_network,        "NET · Network details (--id required)"),
    "network-refs":       (net_network_refs,   "NET · Network references (--id required)"),
    "wifi":               (net_wifi,           "NET · WiFi broadcast (SSID) overview"),
    "wifi-details":       (net_wifi_details,   "NET · WiFi broadcast details (--id required)"),
    "firewall-zones":     (net_fw_zones,       "NET · Firewall zones"),
    "firewall-zone":      (net_fw_zone,        "NET · Firewall zone details (--id required)"),
    "firewall-policies":  (net_fw_policies,    "NET · Firewall policies"),
    "firewall-policy":    (net_fw_policy,      "NET · Firewall policy details (--id required)"),
    "firewall-ordering":  (net_fw_ordering,    "NET · Firewall policy ordering between two zones (--from-zone and --to-zone required)"),
    "acl-rules":          (net_acl_rules,      "NET · ACL rules"),
    "acl-rule":           (net_acl_rule,       "NET · ACL rule details (--id required)"),
    "acl-ordering":       (net_acl_ordering,   "NET · ACL rule ordering"),
    "dns-policies":       (net_dns_policies,   "NET · DNS policies"),
    "dns-policy":         (net_dns_policy,     "NET · DNS policy details (--id required)"),
    "traffic-lists":      (net_traffic_lists,  "NET · Traffic matching lists"),
    "traffic-list":       (net_traffic_list,   "NET · Traffic matching list details (--id required)"),
    "vouchers":           (net_vouchers,       "NET · Hotspot vouchers"),
    "voucher":            (net_voucher,        "NET · Voucher details (--id required)"),
    "wans":               (net_wans,           "NET · WAN interfaces overview"),
    "vpn-tunnels":        (net_vpn_tunnels,    "NET · Site-to-site VPN tunnels"),
    "vpn-servers":        (net_vpn_servers,    "NET · VPN server configurations"),
    "radius":             (net_radius,         "NET · RADIUS profiles"),
    "device-tags":        (net_device_tags,    "NET · Device tags"),
    "dpi-categories":     (net_dpi_cats,       "NET · DPI application categories"),
    "dpi-applications":   (net_dpi_apps,       "NET · DPI applications"),
    "countries":          (net_countries,      "NET · Countries list (for geo-IP firewall rules)"),
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UniFi read-only OpenClaw skill — all traffic via api.ui.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("subcommand", choices=list(COMMANDS) + ["list"],
                        help="Query to run. Use 'list' to see all subcommands.")
    parser.add_argument("--site",        type=str, default=None,
                        help="Site label or partial match (e.g. 'home', 'office', 'udmpro'). "
                             "Run 'library' to see all available labels.")
    parser.add_argument("--id",          type=str, default=None, help="Resource ID")
    parser.add_argument("--limit",       type=int, default=None, help="Max results")
    parser.add_argument("--next-token",  type=str, default=None, help="Pagination token")
    parser.add_argument("--metric-type", type=str, default="1h",  help="ISP metric window: 1h or 5m")
    parser.add_argument("--begin",       type=str, default=None, help="ISP metrics begin (ISO8601)")
    parser.add_argument("--end",         type=str, default=None, help="ISP metrics end (ISO8601)")
    parser.add_argument("--duration",    type=str, default=None, help="ISP metrics duration e.g. 24h")
    parser.add_argument("--from-zone",   type=str, default=None, dest="from_zone",
                        help="Source firewall zone ID — required for firewall-ordering (run firewall-zones to list IDs)")
    parser.add_argument("--to-zone",     type=str, default=None, dest="to_zone",
                        help="Destination firewall zone ID — required for firewall-ordering (run firewall-zones to list IDs)")
    args = parser.parse_args()

    if args.subcommand == "list":
        print(json.dumps({k: v[1] for k, v in COMMANDS.items()}, indent=2))
        return

    COMMANDS[args.subcommand][0](args)


if __name__ == "__main__":
    main()
