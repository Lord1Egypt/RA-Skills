# Day 24 Exposed Anthropic API Key. Rotate now.

**Date:** 2026-04-05
**Filed by:** cc-mini (flagged originally by Lēsa in HEARTBEAT, Day 63)
**Priority:** P0. Security. Caps worst-case cost.
**Repo:** OpenClaw runtime config + 1Password
**Status:** not started. Needs immediate action.

## Problem

On Day 24 (date TBD from Lēsa's memory), an Anthropic API key was exposed. Lēsa flagged it in HEARTBEAT yesterday with: "Rotate that Anthropic API key. Day 24 exposed, and now every token costs money."

Before April 4 noon PT, an exposed OAuth/API key was less urgent because third-party harness calls were covered by the Max subscription regardless of which key was used. After April 4 noon, every token on an exposed key is real pay-as-you-go dollars that can be burned by anyone who has the key.

Parker has not confirmed whether the key is still in use or where it is stored. The key may already be live in:
- `~/.openclaw/agents/main/agent/auth-profiles.json` (Lēsa's auth profile)
- `~/.openclaw/secrets/` (OpenClaw secret storage)
- Environment variable in a cron/LaunchAgent
- 1Password vault as a stored credential
- Any other third-party service Lēsa integrates with

## Blast radius

- **Financial:** any leak equals direct pay-as-you-go billing on Parker's account. At Opus 4.6 rates with Lēsa's context sizes, one malicious session could burn hundreds of dollars in an hour.
- **Reputational:** if the key was committed to a public repo at any point, it may already be scraped by key-harvesting bots.
- **Operational:** if Lēsa's main session depends on this key, rotating it without a replacement in place could take her offline.

## Action plan

### Phase 1. Find the key

- `grep -r "sk-ant-api" ~/.openclaw/ ~/.ldm/ ~/wipcomputerinc/ 2>/dev/null` (known prefix for Anthropic API keys)
- Check 1Password via `op item list --vault "Agent Secrets" | grep -i anthropic`
- Check git history: `cd ~/wipcomputerinc && git log --all -S "sk-ant-api" --source` (to see if it was ever committed)
- Check Lēsa's HEARTBEAT for the original Day 24 entry: search `workspace/memory/*.md` for "Day 24" or "Anthropic key"

### Phase 2. Rotate via Anthropic console

- Log in to console.anthropic.com with Parker's account
- Under API keys, **revoke** the old key (not just delete, revoke)
- Create a new key with the same name + suffix "-rotated-2026-04-05"
- Store the new key in 1Password immediately (do not leave it in terminal scrollback)

### Phase 3. Update all storage locations

- Replace in OpenClaw auth profiles via `openclaw doctor` or direct edit (whichever is canonical)
- Update 1Password entry with the new key as the credential field
- Update any LaunchAgents that inject the key via env var
- Restart OpenClaw gateway to pick up the new key

### Phase 4. Verify Lēsa is operational

- Watch her TUI for the next model call succeeding
- Check HEARTBEAT for any auth errors
- Confirm via Anthropic console that the new key is receiving traffic

### Phase 5. Audit for the root cause of the Day 24 exposure

- How did the key leak? Committed to git? Shared in Slack? Logged to a file?
- Close whatever channel allowed the leak
- Add a pre-commit hook to `wip-file-guard` or `wip-branch-guard` that blocks committing any `sk-ant-api-*` strings

### Phase 6. Alternative: switch to CLI adapter first

If the `@steipete` CLI adapter workaround ships (see `ai/product/bugs/openclaw/2026-04-05--cc-mini--cli-adapter-workaround-steipete.md`), the stored API key becomes dead weight. The CLI adapter does not store a key in OpenClaw config. Rotating the key would still be correct, but the exposure surface drops to zero once the adapter is live.

**Recommended order:** rotate first (fast, safe), then ship CLI adapter (bigger cost win). Do not wait for the adapter to rotate.

## Test plan

1. New key created in Anthropic console
2. Old key revoked in Anthropic console
3. Old key's last-use timestamp in the Anthropic dashboard shows a reasonable window (not recent spikes from unknown sources)
4. New key is in 1Password under the correct vault
5. Lēsa's next turn succeeds
6. Gateway logs show no auth errors
7. Pre-commit hook blocks a test commit with a fake `sk-ant-api-testkey` string

## Cross-references

- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-001.md` Section 5.4
- `ai/product/bugs/openclaw/2026-04-05--cc-mini--cli-adapter-workaround-steipete.md` (orthogonal fix)
- Lēsa's HEARTBEAT entry (Day 63, flagging the key)
- Original Day 24 incident (source document TBD)

## Open questions for Parker

1. Where is the key currently stored? (Needed for Phase 1 targeting.)
2. When was the key exposed and how? (Needed for Phase 5 root cause.)
3. Is the key actively in use or dormant? (Determines urgency of Phase 4.)
4. Should we rotate before or after the CLI adapter ships? (Recommendation above: rotate first.)
