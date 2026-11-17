# Wyckoff — and how this engine reads it

Wyckoff and ICT describe the **same market mechanics** in different words. This skill does not run a second, parallel analysis for Wyckoff — it **relabels the primitives it already computes** (swept liquidity, structure/BOS, the dealing range, volume). That is the whole trick: a "spring" *is* an ICT sweep of the lows; an "upthrust" *is* a sweep of the highs; a "Sign of Strength" *is* a displacement/BOS out of a range.

Every price still comes from the script. The Wyckoff read is **advisory confluence** — it scores in the ticket debate and prints a `Wyckoff:` line, but it never invents a level.

## The method in one screen

**Composite Man.** Read all smart-money activity as one operator who accumulates cheap, marks up, distributes expensive, then marks down. Trade *with* him.

**Three laws.**
1. **Supply & Demand** — imbalance moves price.
2. **Cause & Effect** — time spent building a range is the *cause*; the trend out of it is the *effect*. Bigger base → bigger move.
3. **Effort vs Result** — volume is effort; the price progress it buys is result. Big effort with little result = absorption = a turn is near.

**The cycle:** Accumulation → **Markup** → Distribution → **Markdown**, repeating.

**Accumulation schematic (a bottoming range):**
- **PS** preliminary support · **SC** selling climax · **AR** automatic rally · **ST** secondary test — these carve the range (Phase A/B).
- **Spring / Shakeout** — a dip *below* support that quickly reclaims, grabbing sell-side liquidity and trapping shorts (Phase C).
- **SOS** sign of strength (wide-spread rally breaking the range) · **LPS** last point of support (the higher-low pullback) — Phase D.
- **Markup** out of the range — Phase E.

**Distribution schematic (a topping range)** mirrors it: PSY, **BC** buying climax, AR, ST → **UTAD/Upthrust** (a poke above resistance that fails, Phase C) → **SOW** sign of weakness, **LPSY** last point of supply → **Markdown**.

**Phases A–E:** A stop the prior trend · B build the cause · C the test (spring/upthrust) · D the move begins (SOS/SOW, LPS/LPSY) · E out of the range.

## How the engine maps it (`ict-levels.mjs` → `wyckoff()`)

Output on every analysis as `out.wyckoff`:

| Field | Meaning |
|---|---|
| `schematic` | `accumulation` \| `distribution` \| `markup` \| `markdown` \| `range` \| `transition` |
| `phase` | the Wyckoff phase, boundary-aware — e.g. `Phase C — spring`, `Phase D — demand in control, marking up inside the range`, `Phase E — markup`. **Phase E is only emitted once price has broken OUT of the band** (BOS, or posPct ≥85 / ≤15); a trend bias while still inside the range is Phase D. |
| `event` | the *active* event: `spring` \| `upthrust` \| `SOS` \| `SOW` \| `null` (kept to these five so the debate/dashboard contract is stable) |
| `bias` | `bullish` \| `bearish` \| `neutral` |
| `range` | `{ support, resistance, posPct, widthAtr }` — the H1 trading range |
| `events` | **the event map** — the canonical landmarks read off the swing sequence in time order: `[{ name, price, at, desc }]` where `name` ∈ `SC/BC · AR · ST · Spring/Upthrust · SOS/SOW`, `at` = local-time candle. This is *where the map has been*; it lets the reader see the whole schematic, not just the current label. |
| `location` | **the pinpoint** — one sentence on where price sits *right now* in the schematic (e.g. "supply in control inside the 1.1366–1.1475 range, price at 78%, rolling down from the top toward 1.1366"). Answers "what's happening?" beyond AMD. |
| `nextTell` | the exact trigger that confirms the *next* phase (e.g. "an H1 close below 1.1366 = SOW/breakdown → Phase E"). |
| `effortResult` | volume read on the event bar, where the feed provides volume (indices/metals; FX spot has none) |
| `note` | one-line, copy-ready summary |

### The event map — pinpointing the stage

The engine walks the last ~8 H1 swing highs/lows in **time order** and labels each canonical landmark structurally, so the read says *which stage of the cycle* the asset is in rather than a coarse accumulate/manipulate/distribute:

- **SC / BC** — the climax swing that set the band edge (lowest low = *selling climax*; highest high = *buying climax*), volume-tagged where the feed has it.
- **AR** — the *automatic* move right after the climax that sets the opposite edge (rally after SC, reaction after BC).
- **ST** — the secondary test back toward the climax that holds (higher low in accumulation, lower high in distribution) — supply/demand drying up.
- **Spring / Upthrust** — the Phase-C test (a swept edge that reclaims/fails), reusing the ICT `swept` flag.
- **SOS / SOW** — the Phase-D break of structure out of the range.

`location` then places price against the nearest landmark and `nextTell` names the trigger for the next phase — a reasoning model should narrate these ("we are at the ST of a two-day distribution top; a close under support is the SOW that opens markdown") rather than quoting the fields flatly.

Detection, reusing existing primitives:
- **Trading range** = the band across the last ~8 H1 swing highs/lows; "ranging" if it is bounded (< ~1.4×ATR) and price sits inside with no fresh BOS.
- **Spring** = a **swept sell-side pool at the range low that reclaimed** (the engine's `swept` flag already means *wick beyond + close back inside*), **gated by structure** so a swept low that turned into a breakdown is *not* called a spring.
- **Upthrust** = a **swept buy-side pool at the range high that failed**, gated the same way (a swept high inside a markup reads as strength, not a failed upthrust).
- **SOS / SOW** = an H1 break of structure (`bosUp`/`bosDown`) out of the range.
- **Markup / Markdown** = a clean H1 trend that agrees with H4.
- **Effort vs Result** = the event bar's volume vs the ~60-bar average (only when volume exists).

## How it scores

In the deterministic debate (`debateTicket`), a Wyckoff read that **agrees** with the ticket direction adds a **pro** (`Wyckoff aligned — spring (Phase C)`); one that **opposes** adds a **double-weight con** (`Wyckoff opposes — distribution structure biased bearish`). Structure-gating means it will not fight a strong, trend-aligned setup on a noisy range read.

## For the reasoning layer

When you deep-read a ticket, weave the Wyckoff read into the narrative rather than quoting it flatly: *"this is the spring of a two-day accumulation — the sweep of the lows is Wyckoff Phase C, and the entry sits at the LPS."* A spring backing an ICT bullish sweep-reversal, in a discount, during a killzone, is textbook multi-lens confluence — say so. If Wyckoff and the ICT ticket disagree, that conflict is exactly what the trader needs to hear.
