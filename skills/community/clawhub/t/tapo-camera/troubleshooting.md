# Troubleshooting - Tapo Camera

Use this file when the user already tried a capture or discovery flow and something failed.

## Triage Order

1. Host reachability
2. Camera auth
3. Camera-module availability
4. RTSP and ONVIF enablement
5. `ffmpeg` capture behavior
6. Model-specific fallback needs

## Common Failures

| Symptom | Likely Cause | Better Move |
|---------|--------------|-------------|
| `kasa` cannot connect | wrong host, wrong credentials, LAN mismatch, or device asleep | verify IP, same subnet, and camera account first |
| camera state works but no RTSP URL is usable | third-party compatibility disabled or device class mismatch | check the Tapo app settings and whether the camera is a hub child |
| ONVIF path exists but viewer fails | ONVIF enabled but viewer auth or network path is wrong | verify camera account and test one local ONVIF client |
| `ffmpeg` times out | stream blocked, camera sleeping, or wrong transport conditions | retry once, then test with VLC and reduce assumptions |
| image captures but looks blank or privacy-covered | privacy mode or lens mask enabled | confirm the camera is actually exposing the scene |
| repeated auth failures after firmware changes | camera account drift or changed local compatibility behavior | re-check third-party compatibility settings before rewriting the workflow |

## Diagnostic Moves

- Prefer one deterministic command over broad scanning.
- Check whether the model is direct, battery-powered, or hub-based.
- Compare current behavior against the last known good path if local notes exist.
- If the helper works but another tool does not, the problem is likely downstream of camera auth.

## Escalation Boundary

Stop and restate the trust boundary if the user asks to:
- capture continuously in the background
- expose the camera to the public internet
- upload frames to a third-party AI service
- persist a raw authenticated RTSP URL in a file or ticket
