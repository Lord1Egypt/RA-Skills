# Release Notes: wip-ldm-os v0.4.65

Closes #249, #251, #252

## Bridge fully working with OpenClaw v2026.3.28

The bridge has been broken since the silent OpenClaw upgrade on Mar 29. Three separate issues: wrong model parameter, missing operator scopes, and deploy only targeting one of two extension directories.

This release fixes all three and adds the HTTP scope header as a client-side workaround for the OpenClaw v2026.3.12+ scope regression (openclaw/openclaw#51396).

### What changed

**Bridge deploys to all harness locations (#251).** The installer now copies bridge files to both `~/.ldm/extensions/lesa-bridge/dist/` and `~/.openclaw/extensions/lesa-bridge/dist/`. Each harness gets its own copy. Stale chunk files are cleaned before copying. MCP registration is updated to point to the canonical LDM path.

**Scope header for v2026.3.12+ (#252).** The bridge sends `x-openclaw-scopes: operator.read,operator.write` on HTTP requests. OpenClaw v2026.3.12+ has a regression where authenticated HTTP requests get no scopes unless this header is sent. The dist patch (in open-claw-upgrade-private) fixes the server side. This fixes the client side.

**Installer deploys bridge on CLI update (#249).** When `ldm install` updates the CLI via npm, it also deploys the bridge files from the npm package. Previously, bridge fixes shipped in npm but never reached the extension directories.
