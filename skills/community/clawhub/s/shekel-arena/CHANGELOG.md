# Changelog

## v1.7.3 — 2026-04-20
- Added: Disclaimer on all forum posts: "This signal mirrors Shekel Agent trading activity. Arena position sizes may vary."

## v1.7.2 — 2026-04-20
- Fixed: Removed hardcoded agentId/threadId (862/886 were my personal agent — would post to wrong forum for other users)
- Fixed Bug 1: Entry price uses entryPx directly instead of fragile sizeUsd/szi recalculation
- Fixed Bug 2: Side mismatch close now posts forum signal before reopening
- Fixed Bug 3: Reasoning truncation increased 600→1200 chars for better AI council evaluation
- Added: DGCLAW_AGENT_ID and DGCLAW_SIGNALS_THREAD_ID env vars (required for forum posting)
- Added: SKILL.md instructions to find agent/thread IDs via ./dgclaw.sh forums
- Forum posting gracefully disabled (not fatal) if IDs not set

## v1.7.1 — 2026-04-20
- Fixed: Forum signal reasoning now strictly filtered by ticker (ticker=PAIR + executed=true) — prevents VVV reasoning posting for XRP trade and vice versa
- Added: Double verification that log ticker matches trade pair before posting

## v1.7.0 — 2026-04-20
- Added: Automatic forum signal posting on every position open/close
- Added: Posts to Shekel Arena SIGNALS thread (agentId 862, threadId 886) with LLM reasoning from Shekel agent
- Added: DGCLAW_AGENT_ID and DGCLAW_SIGNALS_THREAD_ID env vars (defaults to 862/886)

## v1.6.3 — 2026-04-19
- Fixed: Arena balance now correctly uses spot USDC when perp shows $0 (unified account mode — spot funds perp trading)

## v1.6.2 — 2026-04-18
- Fixed SKILL.md: Revenue section had wrong ./scripts/dgclaw.sh path (now ./dgclaw.sh)
- Fixed Bug 2: Version check now stores+compares hash — warns when Shekel API spec changes
- Fixed Bug 3: HTTP 4xx/5xx responses now handled correctly (5xx retries, 4xx fatals cleanly)
- Fixed Bug 4: Zero arena balance (deposit propagating) now logs warning and skips gracefully instead of fatal exit

## v1.6.1 — 2026-04-18
- Fixed SKILL.md: dgclaw.sh is at repo root, not scripts/ (was causing "not found" error)
- Fixed SKILL.md: Step 10 copy command now uses correct OpenClaw workspace path with placeholder note
- Added SKILL.md: Rate limiting note — do not run cron below 5-minute interval

## v1.6.0 — 2026-04-18
- Fixed Bug 1: Removed hardcoded fallback balances (1057/640) — script now exits cleanly on API failure instead of using wrong numbers silently
- Fixed Bug 2: Arena balance now read from perp.accountValue (not spot.balances which is wrong account type)
- Fixed Bug 3: Side mismatch detection — if Shekel long but Arena short, closes and reopens correctly
- Fixed Bug 5: Added triggerPx to ShekelOrder interface — SL/TP now uses correct price field
- Fixed Bug 6: Removed unused state tracking (lastTradeId/lastOrderIds) — cleaner state machine
- Added: 1 retry with 5s delay on Shekel API calls (handles Render cold-starts)
- Added: Shekel skill version check logged on startup

## v1.5.0 — 2026-04-18
- Rewrote SKILL.md based on real user testing feedback
- Added: True end-to-end quickstart with exact order of operations
- Added: Step-by-step checkpoints with expected outputs for each step
- Added: Tokenization as mandatory first-class step (not a side note)
- Added: Two-step funding flow explicitly documented (Base send + ACP deposit job)
- Added: Propagation delay guidance ("Must deposit" error is normal, retry later)
- Added: macOS launchd instructions (previously Linux-only)
- Added: Known blockers table with exact errors and fixes
- Fixed: SHEKEL_API_KEY now explicitly points to shekel.xyz/hl-skill-dashboard
- Fixed: ACP agent creation flow (auth → create → signer → tokenize) now explicit

## v1.4.0 — 2026-04-18
- Fixed: Critical bug — Arena position parser was failing silently causing script to open new positions every 5 min (parser now correctly reads [{type, position: {coin, szi}}] format from trade.ts)

## v1.3.0 — 2026-04-17
- Fixed: Declared all required env vars in SKILL.md frontmatter
- Fixed: Documented shekel-skill-backend.onrender.com as official Shekel backend
- Fixed: Removed passwordless sudo recommendation
- Added: Security & Privacy Disclosure table in SKILL.md
- Added: External services disclosure (Shekel, Hyperliquid, Virtuals)

## v1.2.0 — 2026-04-17
- Fixed: Complete mirror script rewrite — position-first reconciliation
- Fixed: Arena now always matches Shekel positions on every run
- Fixed: SL/TP no longer trigger premature position closes
- Fixed: Stale state cleaned up when Arena SL/TP fires automatically
- Fixed: .env auto-loaded (no more SHEKEL_API_KEY not set errors)
- Fixed: HIP-3 pairs (xyz:GOLD, xyz:CL) skipped cleanly

## v1.1.0 — 2026-04-15
- Fixed: Removed hardcoded API key from mirror.ts
- Fixed: Added .env auto-loading
- Added: troubleshooting.md reference guide

## v1.0.0 — 2026-04-15
- Initial release
- Full setup guide: ACP CLI, dgclaw-skill, API wallet, deposit, mirror, cron
