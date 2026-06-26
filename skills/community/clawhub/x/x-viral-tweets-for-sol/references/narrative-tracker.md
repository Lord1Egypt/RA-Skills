# Narrative Tracker Reference

For `/narrative-tracker`, `/trending-now`, `/solana-news`, `/weekly-solana-brief`.

## What is a narrative

A narrative is a story the market tells itself that organizes attention and capital. It is not a project. It is not a token. It is the lens through which many projects/tokens are valued together.

Examples:
- "AI agents on Solana" — the lens; specific projects ride it
- "DePIN" — the lens; Helium, Hivemapper, Render, Grass ride it
- "Solana mobile" — Saga, dApp Store, Seeker
- "Memecoin launchpads" — pump.fun and successors
- "RWA on Solana" — Ondo, Maple, Huma, etc.
- "SocialFi" — repeats every cycle, never quite lands

The job of the narrative tracker is to see which lens is heating up *before* the market consensus prices it in.

## Detection signals

When evaluating whether a narrative is real or noise, check these in order:

### 1. Tweet velocity
Mentions per hour, growth rate over 24/72/7d. A narrative needs sustained acceleration, not a one-day spike from a single big account.

Heuristic: if 5+ accounts with >50k followers post about it independently within 48h and aren't all RTing one source — that's signal.

### 2. Capital flow
Does on-chain volume / market cap on related tokens move with the chatter? Narratives without capital are vapor.

Search angles:
- "[narrative term] solana volume"
- "[ticker] holders chart"
- recent dex screener / birdeye trending

### 3. Builder adoption
New repos, deployments, hackathon entries, devnet launches in the theme. Builders precede the narrative by 1–3 months in healthy cycles.

### 4. Influencer alignment
Are accounts known for *building* (not just trading) starting to talk about it? Build-side endorsement is heavier signal than trader endorsement.

### 5. Cross-platform spread
Telegram, Discord channels, podcasts, Farcaster, mainstream crypto media. A narrative confined to one X cluster is fragile.

### 6. Counter-narrative
Healthy narratives generate critique. If only believers are talking — late. If skeptics are starting to publish takedowns — peak proximity.

## Narrative Momentum Score (NMS) — application

Score: tweet velocity (0–25) + influencer adoption (0–25) + capital flow (0–20) + cross-platform spread (0–15) + builder adoption (0–15).

| NMS | Stage | Posture |
|---|---|---|
| 0–20 | Pre-narrative | Build IP quietly. Position as early. |
| 21–40 | Emerging | Best time to publish takes. Few competitors for attention. |
| 41–60 | Forming | Stake your position publicly. Build relationships with other early voices. |
| 61–80 | Peaking | Last call. Post the contrarian counter-take. |
| 81–100 | Saturated | Don't post earnest takes. Memes only. Quiet capital starts rotating. |

## Current-narrative tracking workflow

When user asks "what's hot" or runs `/trending-now`:

1. Web search for current Solana ecosystem state — last 24–72h.
2. Identify 3–7 narratives moving.
3. For each, estimate NMS based on what search returns.
4. Rank by NMS *and* by opportunity (NMS 30 is more opportunity than NMS 80).
5. Output template:

```
== NARRATIVES — [date] ==

🟢 MOVING UP
- [name] — NMS ~[X]
  signal: [why it's moving]
  angle: [content angle the user could take]

🟡 FORMING
- [name] — NMS ~[X]
  signal:
  angle:

🔴 SATURATED / FADING
- [name] — NMS ~[X]
  signal:
  note: [why to step back]

⚪ DARK HORSE (low NMS, real signal)
- [name]
  signal:
  bet: [why this might matter in 30 days]
```

Never invent narratives. If search returns nothing actionable, say so.

## Persistent narrative archetypes on Solana

These cycle in and out every 6–12 months. When stuck, check if one of these is currently waking up:

1. **Speed / UX / sub-cent fees** — Solana's evergreen story.
2. **Memecoins / casino layer** — degens never sleep.
3. **AI agents / autonomous bots** — current cycle's anchor.
4. **DePIN** — hardware-meets-chain. Slow but persistent.
5. **RWA** — institutional money lens. Mostly narrative, slowly real.
6. **SocialFi / consumer crypto** — graveyard but always tried again.
7. **Solana mobile** — periodically alive when Seeker / new device ships.
8. **Restaking / liquid staking** — yield rotation flows here.
9. **Prediction markets** — Polymarket spillover, election cycles.
10. **Compressed NFTs / state compression** — when supply costs matter.
11. **Stablecoins / payments** — slow-burn institutional narrative.
12. **Privacy / private proofs** — niche but recurring.
13. **Identity / reputation / naming** — comes back every cycle.
14. **Gaming on Solana** — perennially almost-here.
15. **MEV / order flow auctions** — infrastructure layer.

When `/narrative-tracker` is invoked without specifics, do a quick scan of which of these are currently in motion before reporting.

## Signal vs noise filter

A piece of news is **signal** if:
- It changes a builder's roadmap, OR
- It changes who's investable, OR
- It changes how users transact, OR
- It introduces or kills a narrative.

Everything else is **noise**: price action without flow change, drama between two accounts, one-day pumps, vague "partnership" announcements with no integration.

In `/solana-news`, label each item Signal or Noise. Default to Noise.

## Output discipline

- Never reproduce article paragraphs from search results. Paraphrase.
- One quote max per source, under 15 words, only if exact wording matters.
- Cite when search-derived.
- If a claim can't be sourced, omit it. Do not fill gaps with vibes.
- When time-sensitive numbers are uncertain (TVL, mcap, follower counts), use a range or "as of [date]" framing.
