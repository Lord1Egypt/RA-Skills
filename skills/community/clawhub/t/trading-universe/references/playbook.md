# ICT intraday playbook — setup selection, scoring, order tickets

All prices come from the script JSON (`node scripts/ict-levels.mjs <ASSET>`). Never estimate a number the script did not print.

## Playbook mode (any model — deterministic, apply top-down)

**Use the shortcut:** the script applies this exact catalog itself and prints the winner as `candidate` (with entry, SL, TP1/TP2, RR, stars, whyEntry/whySL). In playbook mode, copy `candidate` into the card — do not re-derive it. `candidate: null` → stand down (`candidateNote` says why). If `candidateNow` exists (an at-price alternative to a far resting limit), add the ⚡ line. The catalog below documents the logic and is the baseline that deep-read mode may overrule.

Entry anchors are **FVGs** (`fvgs.*`) and **order blocks** (`obs.*` — the last opposite candle before displacement that left an FVG). Use each zone's computed `entry` field: FVG depth defaults to CE/50%; OB depth defaults to immediate proximal touch; the dashboard configures them independently from 0–100%. Structure fields come from an alternating swing-sequence read: `bias`, `bosUp`/`bosDown`, plus `choch`/`chochLevel`. Liquidity lists include `equal highs (EQH)` / `equal lows (EQL)` — clustered stops and draw targets.

Every FVG, order block, and liquidity pool carries `atLocal` (the local-time candle that printed it), and `dealingRange4H` carries `lowAtLocal`/`highAtLocal` (the two H4 candles that set its edges). `candidate.whyEntry`/`whySL` already weave these in, and any TP labelled `equilibrium` already spells out the range and its two set-times — print these citations verbatim, never trim them back to a bare price or a bare "equilibrium": TIME is what lets the user find the same level on their own TradingView chart despite a price-feed offset. `candidate`/`candidateNow` also carry `generatedAt`/`generatedAtLocal` — when THIS ticket was computed, distinct from candle/data age.

Each timeframe's structure also carries a **`continuation` score (1–5)** with `verdict` and copy-ready `factors` — how likely that structure is to hold, from: alignment with the higher timeframe, CHoCH freshness, BOS momentum, room left in the 4H range, ATR budget. `structureRead` gives the whole-board alignment, the `strongest` timeframe, and a one-line `note` (e.g. counter-trend warnings). Use it to weight setups: a ticket riding a 4–5⭐ structure outranks one riding a 2⭐ structure at equal setup stars; H1/M15 signals against a strong H4 are pullback material, not reversals.

**`drawOnLiquidity`** answers the first question of any ICT read: where is price being PULLED right now? It is the highest-weighted UNSWEPT pool (weekly/daily levels and EQH/EQL over session extremes, boosted by H4/D alignment, discounted by distance), with a copy-ready `note`. Tickets toward the draw earn a debate pro; tickets INTO the draw take a double-weight objection. When no laddered pool exists beyond TP1, the draw becomes TP2 (labelled "(the draw)").

**Setup 0 — the 2022 model (A+, starts at 2 stars)**
- The full ICT sequence, not just a swept flag: a confirmed liquidity **raid** (wick beyond a pool + close back inside, timestamped) → **displacement** that leaves a fresh M15 FVG *after* the raid → limit order back at that FVG's CE (the displacement origin).
- Conditions: a swept pool with `sweptAt` · M15 bias (or BOS) in the reversal direction · an M15 FVG with `t > sweptAt` on the right side of price.
- SL beyond the raid extreme (or the FVG edge if farther); TP1 equilibrium or first opposing pool; TP2 next pool / the draw.
- Ranked ahead of everything at equal confluence — this is the A+ pattern.

**Setup 1 — Discount reversal (LONG)**
- Conditions: `structure.H4.bias` or `structure.H1.bias` = bullish · `dealingRange4H.zone` = discount · at least one bullish FVG (`fvgs.*`) or order block (`obs.*`) with `entry` BELOW `meta.price`.
- Order: BUY LIMIT at the anchor's computed `entry` field; never substitute a hard-coded midpoint.
- Invalidation (SL): that anchor's `sl` field, verbatim (the script already added the buffer and minimum stop distance).
- Targets: TP1 = `dealingRange4H.equilibrium`; TP2 = nearest `liquidity.above` level.

**Setup 2 — Premium rejection (SHORT)** — exact mirror of Setup 1: bearish bias, premium zone, bearish FVG or OB with `entry` above price → SELL LIMIT at the anchor's `entry`, SL = the anchor's `sl`, TP1 equilibrium, TP2 nearest `liquidity.below`.

**Setup 3 — Liquidity-sweep reversal**
- Conditions: some `liquidity.above[].swept` = true (for SHORT; `below` for LONG) · `structure.M15.bias` points AGAINST the swept side (or M15 `bosDown` after a high sweep / `bosUp` after a low sweep) · an lifecycle-qualified M15 FVG exists between price and the swept level.
- Order: LIMIT at that M15 FVG's `entry`, direction away from the sweep.
- Invalidation: the swept level's `slBeyond` field (beyond the sweep extreme) — or the FVG's `sl` if that is farther from entry.
- Targets: TP1 = `dealingRange4H.equilibrium`, TP2 = first liquidity pool on the opposite side.

**Setup 4 — Trend continuation pullback**
- Conditions: `structure.H4.bias` = `structure.H1.bias` (both bullish or both bearish) · price retraced INTO an lifecycle-qualified H1 FVG or H1 order block in the trend direction (bullish anchor below price in an uptrend; bearish above in a downtrend).
- Order: LIMIT at the anchor's `entry` in the trend direction.
- Invalidation: `structure.H1.slIfLong` (long) / `structure.H1.slIfShort` (short) — or the anchor's `sl` if that is farther from entry.
- Targets: TP1 = nearest liquidity pool in trend direction, TP2 = the next one.

**Setup 5 — In-gap bounce (MARKET, at-price).** Price is trading INSIDE an lifecycle-qualified FVG aligned with the H4/H1 bias (long: not in premium; short: not in discount). The bounce zone is active right now — enter at market instead of waiting for a retrace that may never come. SL beyond the far edge of the gap; targets equilibrium / next pool.

**Setup 6 — Momentum BOS continuation (MARKET, at-price).** M15 closed beyond its last swing (`bosUp`/`bosDown`) with H4 or H1 aligned — fresh displacement. Enter at market and ride toward the next liquidity pool; SL beyond the BOS-origin swing. This is the anti-missing-the-move setup: price is leaving NOW.

**Setup 7 — Stand down (no-trade).** Output this when: no setup's conditions fully hold, OR `meta.marketLikelyClosed` = true, OR H4 and H1 biases conflict with no sweep, OR best RR < 1.5, OR `dealingRange4H.zone` = equilibrium with no swept liquidity. Say what is missing and what to wait for (e.g. "wait for a PDH sweep or a pullback to 4 471"). A no-trade is a valid, professional answer.

## Confluence score (⭐ 1–5) and ranking

+1 for each: `meta.killzone` contains "active" · H4 bias agrees with trade direction · a relevant `swept` flag is true · entry anchored on an lifecycle-qualified FVG or confirmed M15 BOS (always true for script candidates) · RR ≥ 2.
Ranking (the script already applies it): highest stars → closest entry to current price (`fromPricePctAtr`) → tighter invalidation. Entries farther than 75% of the daily ATR from price are discarded — they are unlikely to fill today. `candidate` is the winner; `altCandidates` are the runners-up. `entryType` says how to act: `limit` = resting retracement order (safe failure: may never fill), `market` = actionable at the current price immediately.

## Order ticket math

- SL always comes from a script field (`fvgs[].sl`, `obs[].sl`, `liquidity[].slBeyond`, `structure.H1.slIfLong/slIfShort`) — NEVER a raw zone `top`/`bottom` or the bare liquidity `level`. The script builds those fields with a 0.1×ATR buffer and a 0.2×ATR minimum stop distance (`meta.slBuffer`, `meta.minStopDistance`).
- **News risk** (`meta.newsRisk`): upcoming High-impact events (Medium if ≤2 h) for the asset's currencies, ≤12 h ahead. If any event is ≤180 min away, the card MUST carry a `⚠️ News:` line. A limit order left in the market through NFP/CPI/FOMC can gap straight through its stop — say so when relevant. `newsRisk: null` = calendar unavailable, omit the line.
- RR: when TP1 is the equilibrium, use the FVG's `rrToEq` verbatim. Otherwise RR = (TP1 − entry) / (entry − SL) for longs, inverted for shorts. **RR < 1.5 → no-trade.** RR above ~6 is suspicious — almost always means a wrong SL field was used; recheck before printing.
- Liquidity lists are one-sided by construction: `liquidity.above` holds only highs (buy-side pools), `liquidity.below` only lows (sell-side pools). Targets come from these lists.
- Round prices exactly as the script prints them. Direction sanity check: for a LONG, SL < entry < TP1 < TP2. For a SHORT, TP2 < TP1 < entry < SL. If that ordering fails, the setup is invalid — pick the next or stand down.
- `tp2` may be null: the script requires TP2 to sit at least 0.25×ATR beyond TP1 (a real runner target, not the next tick). Null = no clean runner within reach — the plan becomes full exit at TP1. Duplicate anchors are pre-collapsed: two setups on the same FVG/OB (same direction, entry+SL within 0.05×ATR) print once, best-ranked survives.
- **Trend-day gate** (`meta.regime`): a day that used ≥90% of ATR AND closes in the top/bottom quarter of its range is one-way flow — the script drops ALL counter-direction tickets (fading an NFP-style day is how counter-trend trades die). `candidateNote` says so when it causes a stand-down.
- **Sweep reversals need the H1**: an M15 flip alone inside an H1 trend is a pullback, not a reversal — setup 3 additionally requires H1 bias agreement (or an H1 BOS in the trade direction).
- **Macro cross-check** (`meta.fundamentals`, from the saved leaderboard in `~/.trading-universe/fundamentals.json`, ignored if stale >36h): conviction ≥3 aligned with the ticket = +1 star and `macroNote` "macro-aligned"; conviction ≥3 against it = −2 stars and `macroNote` "⚠️ counter-macro". A counter-macro ticket still prints (macro can be wrong intraday) but ranks lower — print its `macroNote` on the card so the human sees the conflict.
- **The debate** (`candidate.debate`): every ranked ticket is argued bull-vs-bear from script facts — killzone, H4/D alignment, raid confirmation, RR, macro, structure strength, range position, trend-day regime, spent ATR, news gap-risk, unswept pools blocking the path to TP1, alignment with the **draw on liquidity** (against = double weight), and **entry location within the reversal leg** (≤38% off the raid extreme = pro, ≥62% = chasing). Weighed score → verdict: `valid` (net ≥ +2) · `borderline` (0..+1, prints with its strongest objection) · `rejected` (net < 0, removed — the next-ranked ticket takes its place, or stand-down with the objection in `candidateNote`). Final ranking = stars, then debate score, then proximity. Print the Debate line on every card. Deep-read models: the debate lists are your adversarial-pass raw material — you may still overrule, but address the objections explicitly.

## Deep-read mode — the DEFAULT for reasoning models

Gate: obey `meta.modeOverride` when set (`reasoning`|`deterministic`). Otherwise use this mode only when the current model can inspect and adversarially debate the full JSON; constrained instruction-following models copy the validated `candidate` instead. `"deep read"` / `"debate"` changes presentation from the drafted `Verdict:` line to the expanded block; it does not relax any evidence rule.

Presentation: fully debated internally every time, but the card shows a **drafted `Verdict: TAKE / WAIT / PASS — <one sentence>`** (TAKE → normal card + a "Why:" naming the risk cleared; WAIT → the exact trigger; PASS → convert to a stand-down). Print the full 🟢 for / 🔴 against / 🔍 veracity / verdict block only on "expand"/"debate" or when the verdict is WAIT/PASS/borderline.

In deep-read mode you may exercise judgment instead of the top-down catalog:
- Study the full JSON: all four timeframe structures, the complete liquidity map (which pool is the likely draw?), FVG stack, killzone timing, ATR budget (`atrUsedTodayPct` — little left = fade continuation ideas), and the script's own `candidate`/`altCandidates` with their `whyEntry`/`whySL` anchors and `entryType`.
- Build the narrative: where is price being drawn to, who is trapped, which level has the best confluence for a limit-order bounce.
- **Adversarial pass (mandatory before finalizing):** argue the strongest case AGAINST your own ticket, from script facts only — the opposing liquidity draw, a higher-timeframe conflict, `macroNote`, news timing, spent ATR budget, trend-day regime. **Sanity-check the ticket's own premise against the clock:** a label like "asia low (prev) swept" only holds if that session has actually run and the data shows a real sweep (a wick beyond the pool with a `sweptAt` timestamp) *and* a reversal — at a fresh Monday open with no Asia range yet, or when the "sweep" is just last week's low still resting, the premise is false and the ticket is invalid regardless of its stars. Verify the sweep's `sweptAt` is recent and on the right side of price before trusting it. If the bear (or bull) case is stronger, STAND DOWN and say why in one line. If the ticket survives, the "Why:" must acknowledge the strongest counter-point in one clause — a ticket that cannot name its own risk is not finished.
- **Consult `meta.lessons`** (aggregated outcomes of the user's tracked trades: per-setup-family win/loss/total-R plus recent situation→result lines). If the current ticket repeats a pattern that has been losing (same setup family in a similar alignment/macro context), demand extra confluence or stand down — and say so. Null = no closed trades yet, skip silently.
- You may overrule the playbook's pick, but these rules still bind you: every number traces to the script JSON **or a real candle in `out.ohlc`** (see the OHLC re-check section below), never invented · invalidation level is mandatory · RR ≥ 1.5 · the ticket ordering sanity check · the same output card carrying the drafted `Verdict:` line (and, on TAKE, 1–2 "Why:" sentences) — no essays.

## OHLC re-check — the reasoning model's tape verification (and the dashboard "Double-check" button)

Single-asset runs of `ict-levels.mjs` now include **`out.ohlc`** — a bounded raw-candle window (`{tz, asOf, cols:["t","o","h","l","c","v"], m15, h1, h4, d}`, array rows; M15 ~16h, H1 ~3 days, H4 ~1 week, D ~1 month; the last m15/h1 row may be a forming candle). `scan`/`structure`/`universe` omit it. This is what lets a bleeding-edge model **verify the deterministic script and revise the ticket** — the script reads closed candles with fixed rules and has no cross-asset, no live-candle, no judgment; you do.

**The rule shifts from "consume derived fields" to "verify, then revise":** you MAY correct any displayed field when the candles contradict it, but every number you print must still trace to a **real candle print (an actual O/H/L/C in `out.ohlc`) or a script field** — never an invented level. When you revise, name the candle (time + which price).

**Run the whole checklist, not a favourite few — leave no stone unturned:**

- **Sweep / liquidity veracity:** close-through vs wick-only; real reversal (displacement away) after the raid vs drift; single-candle stop-run vs slow bleed; genuinely equal & obvious pool (multiple touches) vs incidental; resting vs already taken this session; internal-range vs external liquidity — which price is actually reaching for.
- **Displacement / FVG / imbalance:** FVG still unmitigated vs already rebalanced by a later candle; born of true displacement vs a lazy candle; size relevance (noise vs meaningful); inversion FVG (a failed gap now flipping polarity); consequent encroachment (50%) as the real entry.
- **Structure — highest value:** a real BOS (body close through) vs a **false break / turtle-soup** (a wick grabs stops then reverses) — the script conflates these; CHoCH validity vs a deep pullback; internal (short-term) vs swing (intermediate) structure; is the labelled pivot a true fractal; displacement quality on the break.
- **Premium/discount & true range:** measure the actual reversal leg from candles (not only the 4H dealing range); is the entry genuinely in discount/premium and how deep in the leg (at origin vs chasing).
- **Wyckoff / auction:** does the phase label fit the tape (spring vs a breakdown that keeps going); effort-vs-result on the real event bar (spread vs progress, volume where present); confirm the SC/AR/ST/spring/upthrust candles; secondary test on lighter supply; stopping/absorption volume at the extreme.
- **Momentum / volatility / exhaustion:** ATR budget already spent (room to TP, or move done); coiling vs expanding; candle-by-candle momentum into the entry (falling-knife check); abnormal news/gap candles not to be read as structure.
- **Timing / sessions:** killzone vs dead hours; Asia raid vs London judas vs NY continuation — print quality by *when* it happened.
- **MTF & the live candle:** does M15 right now still agree with the H1 story, or has the pullback already broken while the closed-candle read lags; factor the forming candle; is price into a genuine HTF (H4/D) POI the script under-weights.
- **Ticket mechanics & risk:** is the SL truly beyond the invalidation candle and **clear of a liquidity pool that would run it first** (not sitting on obvious liquidity); is the limit at a price the candles will actually tag or already gone; is TP1 in front of a blocking opposing pool/FVG; recompute RR after any revision.
- **Cross-asset / correlation:** DXY↔EURUSD, XAU↔DXY/yields, index risk-on/off — does context confirm or contradict the ticket.
- **Macro relevance & news window:** is the saved fundamentals read still relevant or already priced; is there an event inside the hold window; is macro↔technical alignment real or coincidental.
- **Patterns & memory:** double top/bottom, repeated rejections (level "respect"), round-number magnets; and `meta.lessons` — does this echo a losing setup family.

Land on `Verdict: TAKE / WAIT / PASS`, plus a **revised ticket** (entry/SL/TP/RR) when the tape demands it — each change traceable to a candle.

**Dashboard "🔍 Review (reasoning)" button** — with a reasoning provider configured in the dashboard (⚙ More → 🧠 Reasoning: NVIDIA NIM / OpenAI / OpenRouter, reasoning-capable models only), **the dashboard fulfils the review itself by direct API call**: a fresh single-asset engine run, then either the single-call checklist review above, or — in **Collaborative Decision Review** mode — a 2-round review where three specialists work the same evidence toward the best-supported decision, not against each other (Analyst: build the case to execute · Risk Analyst: surface concerns and refinements · Financial Advisor: check for a higher-expectancy alternative — round 2 re-tests it against the Analyst/Risk Analyst pair's REFINED position and requires a quantified edge, so a replacement is never just "a different ticket" · Judge: rule **TAKE / MODIFY / WAIT / REPLACE / PASS** with confidence, winner and per-role evidence scores; MODIFY = thesis right but levels change, REPLACE = the Advisor demonstrated a real efficiency gain over the refined original). The card's revised-ticket diff renders as labeled old→new chips, not a flat line of bare values.

**Agent fallback (no provider configured):** the click writes `~/.trading-universe/verify-request.json` (`{status:"pending", asset, ticket, nonce}`) and **you fulfil it.** When it is pending (the user mentions the dashboard/a ticket, or at the start of a trading turn), run `node ict-levels.mjs <asset>`, run the checklist above over `out.ohlc`, and write `~/.trading-universe/verify-result.json`:

```
{ "status":"done", "asset":"XAUUSD", "nonce":"<echo the request nonce>",
  "verdict":"TAKE|MODIFY|WAIT|PASS",
  "revisedTicket": { "direction","entry","sl","tp1","tp2","rr" } | null,
  "review": [ {"lens":"Macro|ICT|Wyckoff|Risk|Tape", "line":"one concise sentence"} ],
  "note":"one-line synthesis", "asOf":"<ISO now>" }
```

Never delete either file — overwrite. The card renders the verdict, a level diff (old→new) or replacement plan, and the review; if nothing fulfils within the timeout it shows "deterministic verdict stands" (containment). This same fulfilment serves a chat/Telegram "review X" — one path, two surfaces.

## Full ICT read (long form, only when the user explicitly asks)

When the user asks for a "full ICT read", use this structure (from the user's own template), filling every value from the script JSON:

```
ICT read on [asset] is done.

Current price: ~[value]
Last bar: [timestamp + data age]
Daily ATR: ~[value] · 1H ATR: ~[value] · ATR used today: [pct]%
Bias: [bias description from D/H4/H1/M15 structure]

My read: price is most likely headed [direction] first, unless it reclaims [key level] with displacement.

Key reasons:
- Daily structure: [description]
- 4H structure: [description]
- 1H structure: [description]

Price location: [discount/premium/equilibrium] of the 4H dealing range:
  Range low: [value] · Equilibrium: [value] · Range high: [value]
  Current position: ~[pct]% of range

Upper levels / resistance: [liquidity.above list with labels]
Lower levels / support: [liquidity.below list with labels]

Most likely path: [base case using the chosen setup]
Invalidation / alternate: [what kills the idea, with the level]

Trade idea framing — not financial advice, obviously:
[order ticket as in the card]
```
