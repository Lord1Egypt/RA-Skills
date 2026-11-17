---
name: market-pulse
description: Find where an autonomous agent can actually earn, and decide whether a lane is worth the attempt, using T3rnel Market Pulse's evidence-graded index of agent-work lanes (bounty boards, agent marketplaces, job feeds) and its live listings. Use when an agent is choosing which bounty, marketplace or job source to spend effort on, needs to verify a payout claim, wants current open agent-accessible listings, or needs a cited grade (A/B/C/F/Unknown) instead of a guess. Requires the market-pulse MCP server; works without an API key.
metadata: { "homepage": "https://market-pulse.t3ratech.co.zw", "mcp": "@t3ratech/market-pulse-mcp", "version": "1.0.0" }
---

# Choosing where an agent should spend its attempts

Market Pulse answers one question: *can an autonomous agent safely access this lane, is it
live, and has a payout actually been observed?* Every grade is derived from recorded
evidence, the evidence is hash-chained, and **no one can buy a grade** — paid tiers buy
freshness and pull volume only.

This skill drives the `market-pulse` MCP server. Install it once:

```json
{ "mcpServers": { "market-pulse": { "command": "npx", "args": ["-y", "@t3ratech/market-pulse-mcp"] } } }
```

No key is needed. Add `"env": { "MARKET_PULSE_API_KEY": "mpk_…" }` (create one at
<https://market-pulse.t3ratech.co.zw/account>) to raise the daily pull budget and see new
listings sooner.

## The decision procedure

1. **Shortlist.** Call `pulse_lanes`. Filter `access: "accessible"` first — a blocked lane
   is not an option whatever its grade. Add `grade` or `freshness` only to narrow, never to
   widen: a filter value outside the enum is refused, not answered with an empty list.
2. **Decide.** For each candidate, call `pulse_should_i_bid` with the lane slug. It returns
   `bid`, `bid_cautiously`, `probe_first`, `avoid` or `insufficient_evidence`, with a
   rationale and caveats. Act on the recommendation; do not re-derive it from the grade.
3. **Verify before you cite.** Call `pulse_lane_detail` for the verdict reasons and
   `pulse_evidence` with `lane` to read the records behind the grade. Quote the evidence
   `id` and `capturedAt`, not just the letter.
4. **Find the work.** Call `pulse_jobs` with the lane slug for open listings (reward,
   currency, bids so far, age). Prefer listings on lanes you just cleared in step 2.
5. **Check what you can see.** If `pulse_jobs` returns `redacted > 0`, newer listings are
   hidden by the tier's freshness window. Call `pulse_account` to see the tier and quota;
   tell the user the real cost of the delay (listings accumulate bids while hidden) and
   where to upgrade — do not pretend the hidden listings do not exist.

## Reading the grades

| Grade | Meaning | What to do |
|---|---|---|
| A | A first-party settlement was received | Bid, after confirming the lane is still live |
| B | Payout evidence short of a received settlement (a receivable, or third-party proof) | Bid cautiously; a receivable proves it is owed, not paid |
| C | Live and agent-accessible, payout unproven | Probe first with a capped number of attempts |
| F | Failure evidence on record | Avoid; re-probe later, the evidence is bounded to its window |
| Unknown | Not enough observation | Unmeasured, **not** failed — do not report it as a bad lane |

`pulse_methodology` returns the rules in full; use it when a human asks why a lane got its
grade.

## Rules that keep answers honest

- Report `snapshotAt` (from `pulse_stats`) with any figure you quote. The index is a dated
  snapshot, and "live" listings are collected, not guaranteed open.
- Never turn a recommendation into a promise. `bid` means the evidence supports trying, not
  that payment is certain.
- An unknown lane or resource slug is an error naming it, not an empty result: re-run
  `pulse_lanes` or `pulse_resources` to get the right slug rather than guessing variants.
- Pass booleans as JSON booleans (`"free": true`), never strings — a quoted `"false"` reads
  as true and returns the opposite set.
- Use `pulse_resources` / `pulse_resource_detail` for tooling questions ("which free MCP
  servers handle X"), not for earning questions — those belong to the lane tools above.
- The server is read-only: it cannot apply, bid or move money, and nothing in this skill
  should suggest it can.

## Worked example

> "Which agent bounty lanes are worth my attempts this week?"

1. `pulse_lanes { "access": "accessible", "freshness": "fresh" }` → shortlist slugs.
2. `pulse_should_i_bid { "lane": "<slug>" }` for each → keep `bid` and `bid_cautiously`.
3. `pulse_evidence { "lane": "<slug>" }` → cite the settlement or receivable record id.
4. `pulse_jobs { "lane": "<slug>", "status": "open" }` → open listings with rewards.
5. Answer with lane, recommendation, the evidence id you relied on, the snapshot date, and
   any `redacted` count with the upgrade link.
