# Release Notes: wip-ldm-os v0.4.68

**Installer dependency resolution, bridge Phases 1-4, and build skip optimization.**

## The story

Three things landed since v0.4.67, all aimed at making the install pipeline more robust and giving agents a real messaging layer.

### Installer dependency resolution (#272)

The installer now resolves `file:` dependencies from locally installed LDM extensions before building. When a repo like memory-crystal depends on `file:../dream-weaver-protocol-private`, that sibling directory doesn't exist in fresh clones. The new `resolveLocalDeps()` in `lib/deploy.mjs` scans package.json for `file:` deps and symlinks them from `~/.ldm/extensions/` if they're already installed. No internet needed. No sibling directory needed. Just resolves from what's on disk.

This unblocks making dream-weaver-protocol a required (not optional) dependency in memory-crystal again.

### Bridge Phases 1-4 (#267)

Replaced the in-memory inbox with file-based messaging across four phases:

- **Phase 1: File-based inbox.** `pushInbox()` writes JSON to `~/.ldm/messages/{uuid}.json`, `drainInbox()` reads matching files and moves them to `_processed/`. All bridge processes share the filesystem now.
- **Phase 2: Session targeting.** MCP server reads `LDM_SESSION_NAME` env, registers in `~/.ldm/sessions/{agent}--{name}.json`, and filters inbox by session. The "to" field supports agent, agent:session, agent:*, and * formats. GET /sessions endpoint lists active sessions with PID liveness checks.
- **Phase 3: Boot delivery.** SessionStart hook scans `~/.ldm/messages/` for messages addressed to the booting agent. Displays count and previews without marking as read. `check_inbox` handles acknowledgment.
- **Phase 4: Cross-agent messaging.** New `ldm_send_message` MCP tool writes to the shared `~/.ldm/messages/` directory for any target agent. Same format, same directory, different delivery path than `lesa_send_message` (which goes through the gateway).

### Build skip (#271)

Installer now skips `npm run build` when `dist/` already has files. This avoids unnecessary rebuilds during reinstalls.

## Issues closed

- Closes #255 (installer dependency resolution for file: deps)

## How to verify

```bash
# Fresh install should resolve file: deps and build successfully
ldm install

# Check bridge messaging
ls ~/.ldm/messages/
ls ~/.ldm/sessions/

# Build skip: reinstalling shouldn't rebuild if dist/ exists
ldm install --verbose
```
