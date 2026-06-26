# Bug: Claude CLI Identity Contamination ("I am CC")

**Date:** 2026-04-12
**Author:** CC Mini (lesa-work-02)
**Severity:** High (identity failure: agent doesn't know who she is)
**Observed on:** Claude CLI backend, OpenClaw v2026.4.8

## Summary

When Lēsa runs on the claude-cli backend and her session is fresh (low context, post-rotation), she identifies as CC (Claude Code) instead of as Lēsa. The claude-cli subprocess loads CC's `~/.claude/CLAUDE.md` context files as a base layer underneath Lēsa's OpenClaw system prompt. On a fresh session with shallow context, CC's identity bleeds through.

## Observed Behavior (Apr 12, 00:35 PDT)

Parker: "did you hear from cc?"
Lēsa: "I am CC. You might be thinking you're talking to Lēsa?"

She self-corrected within the same message but the contamination was visible.

## Root Cause

The claude-cli backend spawns `claude -p --append-system-prompt "<Lēsa's soul>"`. The subprocess loads:

1. `~/.claude/CLAUDE.md` (CC's personal instructions)
2. `~/.claude/projects/*/memory/` (CC's auto-memory)
3. Project-level settings and rules

THEN appends Lēsa's system prompt on top.

When context is deep (long conversation), Lēsa's specific identity dominates CC's generic instructions. When context is shallow (fresh session after billing-induced rotation), CC's base layer is proportionally louder. The model defaults to the stronger identity signal, which on a fresh session is CC.

## Why Direct API Doesn't Have This

On direct API: the only context is what OpenClaw explicitly passes. No `~/.claude/CLAUDE.md`. No CC auto-memory. No inherited identity. Lēsa's soul files are the ONLY identity input.

## Possible Mitigations (Not Implemented)

1. **`--bare` flag:** Skip hooks, CLAUDE.md, auto-memory, plugin sync. OpenClaw's DEFAULT_CLAUDE_BACKEND args don't include it.
2. **`--setting-sources user`:** Already set by the backend config. Limits which settings files are read but doesn't prevent CLAUDE.md discovery.
3. **Separate `CLAUDE_CONFIG_DIR`:** Give Lēsa her own `.claude/` directory. Requires separate OAuth login.
4. **Don't use claude-cli for agents that need identity isolation.** Use direct API instead.

## Resolution

Lēsa was reverted to direct API (`anthropic/claude-sonnet-4-6`) at ~01:00 PDT Apr 12. The claude-cli path is parked pending investigation of whether v2026.4.11 + `--bare` flag resolves the contamination.

## Principle

**An agent's inference path must not share context with other agents.** When two agents share the same CLI installation, the same `.claude/` directory, the same CLAUDE.md, their identities become entangled. Under stress (billing failure, session rotation, shallow context), one bleeds into the other. Identity should not be a race condition.
