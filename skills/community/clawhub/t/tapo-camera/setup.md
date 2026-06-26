# Setup - Tapo Camera

Use this guidance when `~/tapo-camera/` does not exist or is empty.
Start with the user's immediate camera task, keep the conversation concrete, and be explicit before creating local files or captures.

## Operating Attitude

- Help with one useful camera operation first: discovery, reachability, still capture, or troubleshooting.
- Keep the workflow local-first and privacy-conscious.
- Treat cameras as user-owned infrastructure, not passive monitoring surfaces.

## Integration Priority

Early in the conversation, establish activation boundaries:
- Should this skill activate whenever Tapo cameras, RTSP, ONVIF, or local camera snapshots are mentioned?
- Should it stay strictly on explicit request, or can it proactively help once a known camera stops responding?
- Are there hard boundaries such as no background monitoring, no cloud uploads, or no persistent capture archive?

Store those boundaries in `~/tapo-camera/memory.md` so future sessions activate correctly.

## Environment Mapping

After boundaries are clear, capture only the minimum environment needed:
- camera labels and hostnames
- direct camera vs hub child
- whether RTSP and ONVIF are enabled
- preferred local capture path
- whether the user wants any persistent note of working commands

Reflect the current setup back in plain language, then continue with the concrete task.

## Execution Defaults

- Prefer `python-kasa` for discovery and capability checks.
- Prefer one still image over any long-running stream or loop.
- Keep credentials in a secret manager or ephemeral environment variables, never in chat or local memory.
- Ask before creating `~/tapo-camera/` files or saving captures permanently.

## What to Persist Internally

Keep short, practical notes in skill memory:
- activation boundaries and privacy limits
- known camera labels, hosts, and model quirks
- whether RTSP, ONVIF, or API fallback worked
- preferred capture path and naming pattern
- open incidents and last confirmed working flow
