---
name: Tapo Camera
slug: tapo-camera
version: 1.0.0
homepage: https://clawic.com/skills/tapo-camera
description: Connect to Tapo cameras, verify local access, capture snapshots, and inspect frames with local-first RTSP workflows and safe fallbacks.
changelog: Initial release with local discovery, RTSP snapshot capture, device-boundary guardrails, and API fallback guidance for unsupported cases.
metadata: {"clawdbot":{"emoji":"📷","requires":{"bins":["python3","ffmpeg","kasa"],"pip":["python-kasa"],"config":["~/tapo-camera/"],"env.optional":["TAPO_CAMERA_USERNAME","TAPO_CAMERA_PASSWORD","KASA_CREDENTIALS_HASH"]},"install":[{"id":"pip-python-kasa","kind":"pip","package":"python-kasa","bins":["kasa"],"label":"Install python-kasa and the kasa CLI (pip)"},{"id":"brew-ffmpeg","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (Homebrew)"}],"os":["darwin","linux","win32"],"configPaths":["~/tapo-camera/"]}}
---

## When to Use

Use this skill when the user wants an agent to connect to their own Tapo cameras on a trusted local network, verify camera reachability, take still captures, and inspect the resulting frames without defaulting to cloud workflows.

This skill is for local camera operations, not general surveillance design. Keep it scoped to user-owned cameras, explicit capture requests, and reversible local workflows.

## Architecture

Memory lives in `~/tapo-camera/`. If `~/tapo-camera/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/tapo-camera/
├── memory.md               # activation boundaries, preferred capture defaults, and trust limits
├── cameras.md              # hostnames, labels, model notes, and stream capabilities
├── sessions/
│   └── YYYY-MM-DD.md       # capture attempts, failures, and what worked
├── captures/
│   └── ...                 # user-approved local stills only
└── incidents.md            # auth, network, RTSP, and model-specific failure notes
```

Only create `cameras.md`, `sessions/`, `captures/`, or `incidents.md` if the user wants persistent local state.

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status values | `memory-template.md` |
| Camera inventory template | `cameras.md` |
| Incident log template | `incidents.md` |
| Discovery, auth, and capability checks | `discovery-and-auth.md` |
| Local still-capture and review flows | `snapshot-workflows.md` |
| Unofficial API fallback boundary | `api-fallback.md` |
| Failure diagnosis and recovery order | `troubleshooting.md` |
| Local capture helper | `tapo-capture.py` |

## Requirements

- `python3`
- `python-kasa` and its `kasa` CLI for local discovery, device state, and camera module access
- `ffmpeg` for one-frame JPEG capture from RTSP
- A Tapo camera account with RTSP and ONVIF enabled in the Tapo app when the model supports third-party compatibility
- Camera host or IP on the same trusted local network as the agent
- Optional environment variables for the helper: `TAPO_CAMERA_USERNAME`, `TAPO_CAMERA_PASSWORD`, or `KASA_CREDENTIALS_HASH`
- Optional unofficial fallback: a local API library only when RTSP or ONVIF is unavailable and the user approves that narrower path

Treat Tapo credentials and `KASA_CREDENTIALS_HASH` as secrets. Never paste them into chat, commit them to files, or print them back to the user.

## Data Storage

Use local notes only when they improve repeatability:

- the memory file for activation boundaries, privacy limits, and preferred output paths
- `cameras.md` for camera labels, hosts, model quirks, and stream capability notes
- dated session notes for capture attempts and the exact path that worked
- `incidents.md` for recurring auth, RTSP, ONVIF, or firmware regressions
- the `captures/` folder for user-approved still images only

## Core Rules

### 1. Prove scope and ownership before touching a camera
- Confirm the camera belongs to the user and the agent is on the same trusted network segment.
- Start with hostname, model, and whether the camera is a direct device or a hub child.
- Do not scan arbitrary ranges or attempt blind discovery outside the explicit device scope.

### 2. Prefer maintained local tooling first
- Use `python-kasa` and the `kasa` CLI for discovery, auth validation, and camera capability checks.
- Use RTSP and ONVIF on the local camera only after confirming third-party compatibility is enabled.
- Reach for unofficial APIs only when the maintained local path cannot produce the required capture flow.

### 3. Separate discovery from capture
- First prove the device answers and the camera module is present.
- Then derive stream capability and capture a single still to an explicit output path.
- Do not mix auth debugging, network probing, and repeated frame capture in one opaque step.

### 4. Keep secrets out of chat, disk, and process output
- Inject camera credentials from a secret manager or ephemeral environment variables.
- Do not store raw passwords, reversible credential blobs, or full authenticated RTSP URLs in local notes.
- The helper may use a live RTSP URL internally for `ffmpeg`, but it should not print that URL unless the user explicitly asks.

### 5. Capture the smallest useful artifact
- Default to one still image, not continuous recording.
- Write captures only to a user-approved local path under `~/tapo-camera/captures/` or another explicit destination.
- Name captures with camera label and timestamp so later inspection stays deterministic.

### 6. Keep the trust boundary local by default
- Local Tapo device traffic is allowed only to the camera host on the user's LAN.
- Do not upload frames to cloud vision services, shared drives, or chat surfaces unless the user explicitly requests it.
- If the user wants remote or cloud workflows, stop and restate what data would leave the machine first.

### 7. Fall back deterministically
- If `kasa` cannot expose a camera module or RTSP URL, check model support, privacy mode, and third-party compatibility before changing approach.
- If the camera is a hub child, battery device, or a model with broken RTSP support, use the API fallback playbook and keep that path local-first.
- Record the final working path so the next capture does not repeat the same trial-and-error.

## Capture Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Treating every Tapo device like a direct RTSP camera | Hub children and some battery devices do not expose the same local stream surface | Identify device class first, then choose RTSP, ONVIF, or API fallback |
| Printing the full RTSP URL into logs | That leaks camera credentials into history and shared output | Keep URLs redacted by default and only reveal them on explicit request |
| Using cloud login assumptions for local capture | Local device auth and camera account setup are separate in practice | Verify the camera account and third-party compatibility state first |
| Jumping straight to repeated frame pulls | Harder to debug and easier to cross privacy boundaries | Prove one still capture before any loop or batch job |
| Storing captures and credentials together | Raises the blast radius if the local folder is copied or synced | Keep images and secrets separate, and never persist secrets in `~/tapo-camera/` |

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://{camera-host}` | local camera authentication and feature queries | local device connection through `python-kasa` |
| `rtsp://{camera-host}:554/stream1` or `stream2` | local camera credentials and stream request | still capture via `ffmpeg` from the LAN stream |
| `http://{camera-host}:2020/onvif/device_service` | local device-service requests | ONVIF capability checks when enabled on the camera |

No third-party endpoint is part of the default workflow.

## Security & Privacy

Data that may leave your machine:
- Nothing to third parties by default
- Local-LAN requests to the user's camera host for auth, capability checks, and frame capture

Data that stays local:
- User-approved notes under `~/tapo-camera/`
- Captured stills in a local folder chosen by the user
- Troubleshooting logs and device capability notes

This skill does NOT:
- store camera passwords, tokens, or reversible credential blobs in plain text
- capture or upload images without explicit user intent
- run undeclared cloud vision or cloud relay workflows
- modify camera firmware, privacy settings, or motor position by default
- access files outside the working directory or `~/tapo-camera/` for memory

## Scope

This skill ONLY:
- connects to user-owned Tapo cameras on a trusted local network
- validates local access with maintained tools
- captures still images to explicit local paths
- documents the minimum fallback needed when RTSP or ONVIF is unavailable

This skill NEVER:
- brute-force camera credentials or scan arbitrary networks
- enable silent background monitoring
- upload frames to external services by default
- treat hub children, battery devices, and direct cameras as interchangeable
- rewrite the installed skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `cameras` - broader camera capture and review workflows outside the Tapo-specific lane
- `ffmpeg` - deeper frame extraction, transcoding, and media inspection once capture works
- `smart-home` - ecosystem-level device coordination and automation planning
- `iot` - local-device debugging and network-aware connector reasoning
- `photos` - organize and inspect saved captures after acquisition

## Feedback

- If useful: `clawhub star tapo-camera`
- Stay updated: `clawhub sync`
