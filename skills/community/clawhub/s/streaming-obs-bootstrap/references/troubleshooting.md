# Troubleshooting

## Emoji render as broken boxes

- Ensure HTML includes:
  - `<html lang="en">`
  - `<meta charset="UTF-8">`
- Use emoji-safe fonts in CSS stack:
  - `'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji'`

## Browser source blank

1. Verify URL is LAN reachable from OBS host
2. Avoid `file://` for remote OBS setups
3. Recreate browser source with cache-busted URL (`?v=...`)
4. In OBS Browser Source UI, disable hardware acceleration

## OBS connection fails

- Confirm OBS open + WebSocket enabled on port 4455
- Switch target in sqlite config via `obs_target_switch.sh`
- Retry `mcporter call 'obs.get_obs_status()'`

## Smoke test outputs only test card

- Re-run `rebuild_scenes.sh` to attach real overlays
- Verify files exist under `streaming/overlays/`
