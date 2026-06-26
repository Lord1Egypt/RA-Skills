---
name: walvis-message-handler
description: WALVIS hook that fast-routes deterministic /walvis commands and auto-routes bookmark saves without explicit /command
metadata:
  {
    "openclaw":
      {
        "events": ["message:received", "message:preprocessed"],
        "always": false,
      },
  }
---

# WALVIS Message Hook

This hook handles two responsibilities:

1. **Fast-path routing for deterministic commands**:
   - Uses `~/.walvis/manifest.json` `fastPathEnabled` when present.
   - Defaults to ON for first-run flows when the manifest does not exist yet.
   - Can also be forced on with `WALVIS_FASTPATH=1`.
   - Rewrites `/walvis` subcommands into plugin auto-reply commands so these flows bypass LLM inference:
     - bare `/walvis` -> `/walvis-list`
     - `/walvis list ...` -> `/walvis-list ...`
     - `/walvis search ...` -> `/walvis-search ...`
     - `/walvis sync` -> `/walvis-sync`
     - `/walvis spaces | new | use | status | balance | web | help` -> matching `walvis-*` commands
     - `/walvis encrypt | share | unshare | seal-status` -> matching `walvis-*` commands
     - `/walvis +tag | +note | cancel` -> matching `walvis-*` commands
   - If a tag/note edit is pending, the next non-command message is rewritten to `/walvis-pending ...`.
   - Legacy `w:*` callback payloads are rewritten to `/walvis-callback ...`.
   - The `walvis-fastpath` plugin returns Telegram inline keyboards directly via `channelData.telegram.buttons`, so list/search pagination and item actions stay deterministic too.

2. **Auto-save URL routing**:
   - On `message:received`, if `autoSave` is enabled and a message is a bare URL, rewrite it to `@{agent} {url}`.

## Behavior

When a received message:
- contains only a URL (no other text)
- and the user has previously set auto-save mode

Then the hook triggers the save pipeline as if they had typed `@walvis <url>`.

This hook should stay lightweight — if the message does not match, it should do nothing.
