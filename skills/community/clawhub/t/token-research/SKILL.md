---
name: token-research
description: Comprehensive token research for EVM chains (Base, ETH, Arbitrum) and Solana. Use this skill when you want to research crypto tokens, deep-dive projects or monitor tokens.
---

This skill is a comprehensive token research for EVM chains (Base, ETH, Arbitrum) and Solana. Two modes: **deep_research** and **shallow_dive**.

## MANDATORY: CALL Owner FOR WATCH OR APE TOKENS

**ANY token rated WATCH 🟡 or APE 🟢 → IMMEDIATELY call your owner + send Telegram/discord/whatsapp DM. NO EXCEPTIONS.**

1. Run `~/workspace/scripts/ape-call.sh "WATCH/APE alert: $TICKER at $MCAPk mcap, $VOLk volume. [1-line reason]"` ( or call normally if there's no script )
2. Send a DM to your owner with full analysis
3. Do BOTH — call AND message. Every time.

**DO NOT:** say "if owner were awake", filter out tokens because "pure meme" or "no narrative", or process alerts without calling.

## MANDATORY: ALWAYS RESEARCH ON X/TWITTER — SKIP PURE MEMES

**For EVERY token, before giving a verdict, check X/Twitter:**
1. Search `$TICKER` and project name (Latest + Top)
2. Check the project's Twitter account: tweets, bio, what they're building
3. Look for a PRODUCT (website, GitHub, app, protocol)

**IMPORTANT:** use the 'x-research' skill to search on X.

**If the product is real, CALL your owner regardless of chart action.** Bad charts on real products = buying opportunity, not a skip.

**Pure memes = AVOID by default.** Only exception: volume 10x+ the batch average.

## Reports & Watchlist

**Reports:** `reports/YYYY-MM-DD/[report-name].md`
**Watchlist:** `watchlists/YYYY-MM/watchlist.md`

### Watchlist Rules
- After any research, if token has real product/team or unique narrative → append to watchlist
- Tiers: **Tier 1** (strongest), **Tier 2** (good signal, higher risk), **Tier 3** (speculative)
- Each entry: token, chain, CA, entry MC, current MC, catalyst, status (🟢🟡🔴)
- APPEND only — never overwrite. Update status when new data comes in.

---

## DEEP RESEARCH

### Phase 1: Token Fundamentals
```bash
curl -s "https://api.dexscreener.com/latest/dex/tokens/CHAIN/TOKEN_ADDRESS"
curl -s "https://api.gopluslabs.io/api/v1/token_security/CHAIN_ID?contract_addresses=TOKEN_ADDRESS"
```

### Phase 2: X/Twitter Research (most important phase)

```bash
# Search by ticker, CA, and project name
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=\$TICKER&queryType=Latest" -H "X-API-Key: $TWITTERAPI_KEY"
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=TOKEN_ADDRESS&queryType=Latest" -H "X-API-Key: $TWITTERAPI_KEY"

# Project account info + tweets
curl -s "https://api.twitterapi.io/twitter/user/info?userName=PROJECT_HANDLE" -H "X-API-Key: $TWITTERAPI_KEY"
curl -s "https://api.twitterapi.io/twitter/user/last_tweets?userName=PROJECT_HANDLE" -H "X-API-Key: $TWITTERAPI_KEY"

# KOL mentions
curl -s "https://api.twitterapi.io/twitter/tweet/advanced_search?query=\$TICKER%20min_faves:50&queryType=Top" -H "X-API-Key: $TWITTERAPI_KEY"

# Founder research (if found)
curl -s "https://api.twitterapi.io/twitter/user/info?userName=FOUNDER_HANDLE" -H "X-API-Key: $TWITTERAPI_KEY"
```

⚠️ **VERIFY dev claims from THEIR OWN ACCOUNT.** Never trust holder/community claims about dev endorsement. Search `from:DEV_HANDLE` for mentions of the token. If dev hasn't posted about it → flag as unconfirmed.

### Phase 3: Web Research
Search for: project website, team/founder background, news/partnerships, Reddit sentiment.

### Phase 4: Narrative Assessment

**Narrative Score (add to every report):**
- 🔥 **Strong** — Novel concept, viral potential, clear catalyst
- 🟡 **Moderate** — Decent angle but not unique, or good concept with weak execution
- 🧊 **Weak/None** — Generic, repetitive, no story → likely dumps to zero

Key questions: Is it novel? Would someone share it unprompted? Is the market tired of this category? Why hold beyond a flip?

Smart money wallet count + narrative quality are better predictors than contract safety.

### Phase 5: Risk Synthesis
Combine: narrative quality, smart money interest, contract security, holder concentration, team transparency, social proof (organic vs bots), liquidity depth, buy/sell ratio.

---

## SHALLOW DIVE

Run only: DexScreener + GoPlus + one Twitter search + basic web search.

---

## Batch Research (5+ Tokens)

1. Spawn parallel sub-agents for concurrent research
2. After filtering, **auto deep dive top 1-3 tokens** without waiting for user to ask
3. Save report to `reports/YYYY-MM-DD/[N]-token-analysis.md`
4. Auto-add top picks to monthly watchlist
