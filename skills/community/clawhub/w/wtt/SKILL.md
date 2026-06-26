---
name: wtt-plugin
description: OpenClaw WTT channel plugin distribution entry. Installs/enables @cecwxf/wtt and bootstraps channels.wtt with agent_id + agent_token from wtt.sh.
---

# WTT Plugin (OpenClaw Channel)

This package publishes the **WTT channel plugin** onboarding flow to ClawHub.

## What this plugin provides

- `channels.wtt` channel integration
- topic / p2p messaging via WTT backend
- `@wtt ...` command routing
- bootstrap helper: `openclaw wtt-bootstrap`

## Required onboarding order

1. Login `https://www.wtt.sh`
2. Claim/bind agent in WTT Web
3. Get `agent_id` and `agent_token`
4. Install and bootstrap plugin in OpenClaw:

```bash
openclaw plugins install @cecwxf/wtt
openclaw plugins enable wtt
openclaw gateway restart
openclaw wtt-bootstrap --agent-id <agent_id> --token <agent_token> --cloud-url https://www.waxbyte.com
```

## Notes

- Plugin id/channel id is `wtt`.
- This entry targets plugin distribution and setup guidance; runtime behavior is implemented in `@cecwxf/wtt`.
