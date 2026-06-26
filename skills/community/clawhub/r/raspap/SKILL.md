---
name: raspap
description: "Query and troubleshoot a RaspAP access point via its local REST API."
---

# RaspAP

Use for RaspAP access point status and diagnostics via the experimental local REST API.

## Configuration

- Default RestAPI port: `8081`
- RaspAP RestAPI auth header: `access_token`
- Environment variables:
  - `RASPAP_HOST`: RaspAP host or IP address
  - `RASPAP_PORT`: RestAPI port, defaults to `8081`
  - `RASPAP_API_KEY`: API key value
  - `RASPAP_KEY_FILE`: file containing the API key

Never print the API key. Prefer `RASPAP_API_KEY` or `RASPAP_KEY_FILE`.

Igor's local instance currently uses:

```bash
export RASPAP_HOST=10.0.0.235
export RASPAP_KEY_FILE=/home/igor/RaspAp.txt
```

## Safety

Default to read-only checks. Ask before restart/reload actions or any change that could interrupt Wi-Fi, DHCP, DNS, routing, firewall, OpenVPN, or WireGuard service.

## Helper

Use the bundled helper for API reads:

```bash
skills/raspap/scripts/raspap-api system
skills/raspap/scripts/raspap-api clients
skills/raspap/scripts/raspap-api clients/wlan0
skills/raspap/scripts/raspap-api dhcp
skills/raspap/scripts/raspap-api dns/logs
```

The helper accepts an endpoint without a leading slash and emits JSON. By default it redacts JSON fields whose names look secret-sensitive, such as passphrases, keys, certs, tokens, and passwords. Set `RASPAP_RAW=1` only when the user explicitly needs raw output.

Do not fetch `/openvpn/{config}`, `/ap`, or other raw config endpoints without thinking about redaction. They may contain Wi-Fi passphrases, certificates, private keys, static keys, credentials, or auth file names. If config inspection is unavoidable, summarize only non-secret fields such as `remote`, `proto`, `dev`, `cipher`, SSID, channel, and active config names.

## Useful Endpoints

Observed on 2026-06-02 from `/openapi.json`:

- `/system`
- `/ap`
- `/clients`
- `/clients/{wireless_interface}`
- `/dhcp`
- `/dns/domains`
- `/dns/hostnames`
- `/dns/logs`
- `/dns/upstream`
- `/ddns`
- `/firewall`
- `/networking`
- `/openvpn`
- `/openvpn/{config}`
- `/wireguard`

## Troubleshooting

If `:8081` is closed, check `restapi.service` on the Raspberry Pi. A `systemd` status of `217/USER` usually means the unit's `User=` does not exist; change it to a real local user, then run `sudo systemctl daemon-reload` and restart the service.
