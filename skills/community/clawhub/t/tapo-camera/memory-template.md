# Memory Template - Tapo Camera

Create `~/tapo-camera/memory.md` with this structure:

```markdown
# Tapo Camera Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Context
- Activation boundaries for Tapo-camera work.
- Trusted local network assumptions and privacy limits.

## Cameras
- Known camera labels, hosts, model names, and whether they are direct cameras or hub children.
- Whether RTSP, ONVIF, or API fallback is currently working.

## Capture Defaults
- Preferred output directory and filename pattern.
- Whether captures should be transient or saved.

## Notes
- Troubleshooting breadcrumbs, model-specific quirks, and last confirmed working command.

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | environment still being mapped | capture new camera details only when useful to the active task |
| `complete` | stable local workflow exists | reuse the stored host, path, and capability notes |
| `paused` | user paused persistence | read memory but do not add new notes |
| `never_ask` | user does not want setup prompts | stay stateless unless the user explicitly requests persistence |

## Key Principles

- Keep entries operational and concise.
- Store host labels and workflow outcomes, not secrets.
- Do not store passwords, reversible credential blobs, or full authenticated RTSP URLs.
- Update `last` after confirmed memory writes.
