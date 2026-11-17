# XPAI Discovery

XPAI private protocol discovery — `scripts/toolkit/discovery.py`

> **MCP-only:** Device discovery is performed exclusively through the MCP tool `search_devices()` (in `device_mgmt.py`). This module (`discovery.py`) is an internal implementation detail — never import it directly or reference its functions.

---

## How Discovery Works (Internal)

`search_devices()` internally dispatches to the appropriate discovery protocol based on the `method` parameter (or auto-selects when omitted):

| Protocol | Transport | What it finds |
|----------|-----------|---------------|
| WS-Discovery (ONVIF) | Multicast (standard ONVIF) | All ONVIF cameras (including XPAI) |
| XPAI private (SK) | UDP broadcast/unicast | Skyworth devices only (richer metadata: SN, channels, MAC) |
| JCP | UDP multicast `230.230.230.230:8002` + per-interface subnet broadcast, fixed bind port 8002 | JCP devices; SN parsed from the `Device-VerKernel` reply field (portion before the dash) |

USB webcams are **not supported** by this skill — there is no USB enumeration and no USB streaming path; LAN IP cameras (ONVIF/RTSP) only.

Results are normalized into a unified `DiscoveredDevice` structure. XPAI-specific fields (SN, subtype, channels, MAC, etc.) are populated under `sky_*` prefixed attributes when the XPAI protocol is used.

**Protocol classification (`protocol_type`):** each `DiscoveredDevice` carries a `protocol_type` field — **`S`** (answered SK private discovery — conclusive) or **empty** (found via JCP/WS-Discovery; no class asserted). Providers run sequentially in the order SK → JCP → WS-Discovery, and results are merged first-wins by IP. `connect_device` resolves and persists the final class (`S`/`J`/`O`) via an authoritative SK-first unicast probe — a JCP answer alone cannot prove J-class, because JCP discovery is shared by both S- and J-class firmware; `O` (third-party ONVIF-only, degraded) is asserted only at connect time when SK/JCP probes are empty and the ONVIF admission probe passes.

**Registry sync (search is a write operation):** every `DiscoveredDevice` also carries `rtsp_access`, the main-stream reachability probe result (`open` / `auth_required` / `unreachable`). After discovery, `search_devices()` registers each reachable device into `config.yaml` (basic info only, never a password) and removes registered entries that were neither discovered nor reachable. If any provider failed, registration still runs but removal is skipped.

