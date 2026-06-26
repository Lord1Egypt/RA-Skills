# Networking Notes

## Host layout

- Agent machine serves overlays over HTTP on `:8787`
- OBS machine (local/remote) loads browser sources from agent LAN IP

## Validation checks

1. Confirm server listening:
   - `ss -ltnp | grep :8787`
2. Confirm local reachability:
   - `curl -I http://127.0.0.1:8787/streaming/overlays/intro.html`
3. Confirm OBS target set:
   - `mcporter call 'obs.get_obs_status()'`

## Common issue

If browser sources are blank in OBS but page loads in browser:
- disable hardware acceleration in Browser Source properties
- refresh cache / recreate source
- verify no firewall blocks OBS host from reaching agent LAN IP
