# UniFi API Endpoint Reference

Tested against: UniFi OS Server v5.0.6 / Network App v10.2.105

Base: `https://<unifi-os-host>`
Auth: `X-API-Key: <key>` header
Site: `/proxy/network/api/s/{site}/` or `/proxy/network/v2/api/site/{site}/`

---

## ⚠️ Response Shape Difference

| Endpoint | Response wrapper | Key |
|----------|-----------------|-----|
| **v2 device** (`/v2/api/site/{site}/device`) | `{}` **not** wrapped | `.network_devices[]` (managed), `.unmanaged_devices[]` |
| **All legacy** (`/api/s/{site}/...`) | `{"data": [...]}` | `.data[]` |

The v2 endpoint does NOT use `{"data": [...]}`. All scripts use `( .network_devices // .data )[]` pattern.

---

## Inventory (TTL: 3600s)

| Endpoint | Response key | Used by |
|----------|-------------|---------|
| `GET /proxy/network/v2/api/site/{site}/device` | `.network_devices[]`, `.unmanaged_devices[]` | devices.sh, snapshot.sh, device_detail.sh, client_locate.sh, firmware.sh, topology_export.sh |
| `GET /proxy/network/api/s/{site}/rest/networkconf` | `.data[]` | networks.sh, snapshot.sh, client_locate.sh, topology_export.sh |
| `GET /proxy/network/api/s/{site}/rest/wlanconf` | `.data[]` | wlans.sh, topology_export.sh |
| `GET /proxy/network/api/s/{site}/rest/portconf` | `.data[]` | port_profiles.sh |
| `GET /proxy/network/api/s/{site}/rest/portforward` | `.data[]` | port_forwards.sh, topology_export.sh |

## Operational (TTL: 300s)

| Endpoint | Response key | Used by |
|----------|-------------|---------|
| `GET /proxy/network/api/s/{site}/stat/health` | `.data[]` (subsystem objects) | health.sh, snapshot.sh, topology_export.sh |
| `GET /proxy/network/api/s/{site}/stat/sta` | `.data[]` | clients.sh, snapshot.sh, client_locate.sh |
| `GET /proxy/network/api/s/{site}/stat/alluser?within=N` | `.data[]` | client_history.sh |
| `GET /proxy/network/api/s/{site}/stat/sitedpi` | `.data[]` | dpi.sh |

## Alerts (TTL: 60s)

| Endpoint | Response key | Used by |
|----------|-------------|---------|
| `GET /proxy/network/api/s/{site}/stat/alarm?archived=false` | `.data[]` | alerts.sh, snapshot.sh |
| `GET /proxy/network/api/s/{site}/stat/alarm?archived=true` | `.data[]` | alerts.sh --archived |

---

## Health Subsystem Status Notes

- **WAN**: Returns `"unknown"` when no UniFi gateway is adopted (e.g. TNSR/other router). `num_gw: 0` in this case. This is normal for non-UniFi routers.
- **LAN**: `"error"` when `num_disconnected > 0` (disconnected switches/APs). Check `num_disconnected` field for count.
- **WLAN**: `"ok"` when APs are connected and healthy. `"error"` when `num_disconnected > 0`.
- **WWW**: `"unknown"` if not applicable — not used in most setups.

## Device State Values

| State | Meaning |
|-------|---------|
| `1` | Online / adopted |
| `0` | Offline / disconnected |
| Other | Other states (provisioning, etc.) |

## Notes

- All endpoints are GET only. No write operations.
- v2 device endpoint returns richer port/radio data than legacy `stat/device`.
- `stat/alluser` requires Network App to have client history enabled (Settings → System → History).
- `stat/sitedpi` returns empty if Deep Packet Inspection is not enabled in Traffic Management.
- API key must have at minimum: Network read scope.
- Config: set `UNIFI_URL` and `UNIFI_API_KEY` environment variables, or create a config file per `SKILL.md`.
