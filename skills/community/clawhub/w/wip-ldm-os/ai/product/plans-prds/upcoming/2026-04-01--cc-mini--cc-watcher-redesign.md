# Plan: cc-watcher Redesign

**Date:** 2026-04-01
**Author:** cc-mini (with Parker)
**From bug:** 2026-03-30--cc-mini--cc-watcher-retire.md (archiving after this plan is created)

## Context

cc-watcher was a LaunchAgent that monitored Claude Code sessions, auto-approved permission dialogs via screen scanning (Peekaboo), and checked the lesa-bridge inbox. It broke during the Mar 24 migration (old iCloud paths) and was disabled on Mar 30.

Parker's decision: don't retire. The agent-to-agent communication channel is still needed. But redesign it. The Peekaboo screen-scanning approach was fragile (required screen recording permissions, only worked when Terminal was visible).

## What's already done

- **Broken LaunchAgent disabled.** `ldm install` renames `com.wipcomputer.cc-watcher.plist` to `.disabled`. Running. Verified.
- **Monitoring covered.** `ai.openclaw.healthcheck` handles gateway monitoring, HTTP probes, token usage.
- **Inbox covered (partially).** Bridge Phases 1-4 built (file-based inbox, session targeting). tmux works for Lesa-to-CC. HTTP inbox at 18790 works for posting. The gap: no persistent polling on CC's side.

## What the redesign should be

NOT screen automation. NOT Peekaboo. A proper message channel.

### Option A: File-based inbox with boot check (simplest)
- Lesa writes to `~/.ldm/agents/cc-mini/inbox/` (already built in Phase 1-4)
- CC's SessionStart hook checks inbox on boot (already built in Phase 3)
- No daemon. No LaunchAgent. Just files and a boot hook.
- Limitation: CC only sees messages when a new session starts. No real-time.

### Option B: Polling daemon (like the old cc-watcher but simpler)
- LaunchAgent runs a lightweight script every 30 seconds
- Checks `~/.ldm/messages/` for messages to cc-mini
- If found: sends notification, writes to tmux if a session exists
- Advantage: real-time delivery
- Disadvantage: another LaunchAgent to manage

### Option C: tmux watcher (current workaround)
- Lesa uses `tmux send-keys` to type into CC's session
- Works today. Proven in the bridge demo.
- Limitation: requires tmux. Requires knowing the session name.

### Recommendation

**Option A for now. Option B later.**

The file-based inbox with boot check is already built (Phase 3 of bridge plan). It covers 90% of the use case. The polling daemon (Option B) is Phase 5 future work. tmux stays as the interactive fallback.

No new LaunchAgent needed. No daemon. No screen scanning. Just the bridge infrastructure we already built.

## What needs to happen

1. Verify Phase 1-4 of bridge messaging works end-to-end (file-based inbox)
2. Verify SessionStart boot hook shows pending messages
3. Document the new communication paths in the bridge docs
4. Close the cc-watcher bug

## Relationship to other plans

- Bridge Phases 1-4: `ai/product/plans-prds/bridge/2026-03-30--cc-mini--bridge-messaging-architecture.md`
- Bridge Phase 5 (Cloud Relay): `ai/product/plans-prds/bridge/2026-03-31--cc-mini--phase5-cloud-relay.md`
- iOS app as Core: `ai/product/plans-prds/bridge/2026-03-30--cc-mini--ios-app-as-core.md`
