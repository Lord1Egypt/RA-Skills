# Metric Presentation Style Guide

> **CRITICAL:** All skill output must mirror the Rankscale app's metric presentation exactly.

---

## Core Principle

Users see metrics in the Rankscale app dashboard. The skill output should look and feel the same — same terminology, same formatting, same trends interpretation.

---

## Metric Card Format (ASCII)

All metrics follow this visual pattern:

```
┌─ [Icon/Label] Metric Name ──────────────────┐
│  Trend: [↑ +3.2% | ↓ -1.8% | → No change]   │
│                                              │
│         69.1                                 │
│    (Large, primary value)                    │
│                                              │
│    Out of 12 AI engines                      │
│ (Secondary context, lowercase)               │
│                                              │
│ ▁▂▃▄▅▆▇█ ▇▆▅▄▃▂▁ (sparkline data)           │
│ Trend: ↗ Improving over 7 days               │
└──────────────────────────────────────────────┘
```

---

## Individual Metrics

### Visibility Score

**From app:**
- Title: "Visibility Score"
- Main value: Large number (1 decimal), e.g., "69.1"
- Trend: `current - previous` (e.g., "+0.7", "-1.2")
  - `+X%` = green ↑ (improving)
  - `-X%` = red ↓ (declining)
  - `0.0%` = gray → (unchanged)
- Secondary: "Out of 12 engines" or "Vs X AI search engines"
- Icon: Eye 👁️

**Skill output format:**
```
📊 Visibility Score
Trend: ↑ +0.7 (improving)

     69.1
  Out of 12 AI engines

Weekly trend: ↗ Improving
Last 7 days: 68.4 → 69.1
```

---

### Detection Rate

**From app:**
- Title: "Detection Rate"
- Main value: Percentage (1 decimal), e.g., "79.2%"
- Trend: `+X%` or `-X%` with color
- Secondary: "Detected in X engines" or "Detection rate"
- Icon: Target/Crosshair 🎯

**Skill output format:**
```
🎯 Detection Rate
Trend: ↑ +2.1%

     79.2%
  Detected in 10 engines
```

---

### Sentiment

**From app:**
- Title: "Sentiment"
- Main value: Score (1 decimal), e.g., "74" or "74/100"
- Trend: `+X` or `-X` points
- Secondary: "Positive sentiment ratio" or "Brand sentiment score"
- Icon: Smile/Heart 😊

**Skill output format:**
```
😊 Sentiment
Trend: ↑ +3 points

     74/100
  Positive mentions dominate
```

---

### Mentions

**From app:**
- Title: "Mentions"
- Main value: Count (no decimals, comma-separated), e.g., "2,189"
- Trend: `+X` or `-X` absolute count
- Secondary: "Total mentions across engines"
- Icon: Message 💬

**Skill output format:**
```
💬 Mentions
Trend: ↑ +147

     2,189
  Across all engines
```

---

### Citations

**From app:**
- Title: "Citations"
- Main value: Count (no decimals, comma-separated), e.g., "4,057"
- Trend: `+X` or `-X` absolute count
- Secondary: "Links from external sources"
- Icon: Link 🔗

**Skill output format:**
```
🔗 Citations
Trend: ↓ -23

     4,057
  From external sources
```

---

### Average Position (Rank)

**From app:**
- Title: "Avg. Position"
- Main value: Position number with # prefix (1 decimal), e.g., "#2.1"
- Trend: **IMPORTANT** — Negative delta is GOOD here!
  - `-X` = green ↑ (ranked higher, moved up)
  - `+X` = red ↓ (ranked lower, moved down)
  - `0` = gray → (no change)
- Secondary: "Average ranking position"
- Icon: Ranking 📍

**Skill output format:**
```
📍 Avg. Position
Trend: ↑ -0.3 (improved, moved up)

     #2.1
  Average ranking position
```

---

## NEW: Reputation Score (from Research)

**Style:** Mirrors Sentiment, follows same patterns

- Title: "Reputation Score"
- Main value: Score (1 decimal), e.g., "85.2/100"
- Trend: `+X` or `-X` points (improving/declining)
  - `+X` = green ↑ (improving)
  - `-X` = red ↓ (declining)
- Secondary: "Brand sentiment and impact"
- Icon: Shield 🛡️

**Skill output format:**
```
🛡️  Reputation Score
Trend: ↑ +4.2 (improving)

     85.2/100
  Strong positive brand perception

Risk areas: pricing (3x), support (2x)
Top strengths: innovation (8x), reliability (6x)
```

---

## Colors in ASCII Output

When possible, use these inline markers (for terminals that support ANSI):

```
✅ Green (positive):    ↑ or +X or 🟢 (improving, good)
❌ Red (negative):      ↓ or -X or 🔴 (declining, bad)
⚫ Gray (neutral):      → or 0.0 or ⚪ (no change)
🔵 Blue (primary):      Main metric values, headers
```

Terminal output example:
```
📊 Visibility Score         🟢 ↑ +0.7
                            
     69.1
  Out of 12 engines

🎯 Detection Rate           🟢 ↑ +2.1%

     79.2%
  Detected in 10 engines
```

---

## Terminology (Do NOT Change)

| Use | Don't use |
|-----|-----------|
| Visibility Score | Visibility or Score |
| Detection Rate | Detect rate or Matches |
| Sentiment | Sentiment score or Opinion |
| Mentions | Brand mentions or Impressions |
| Citations | External citations or Backlinks |
| Avg. Position | Position or Rank or Average rank |
| Reputation Score | Rep score or Trust score |
| Out of X engines | In X engines or Across X |
| Vs X AI search engines | Compared to X or Against X |

---

## Secondary Text Guidelines

Always include context that explains **what** the number means:

✅ **Good:**
- "Out of 12 engines"
- "Detected in X engines"
- "Across all AI search engines"
- "Positive brand mentions"
- "From external sources"
- "Average ranking position"

❌ **Bad:**
- "ownBrandMetrics.visibilityScore" (technical jargon)
- "12 engines"  (missing "out of")
- "4057 citations" (no formatting, no context)
- "Normalized to 0-100" (too technical)

---

## Trend Delta Rules

### Positive Metrics (higher is better)
- Visibility Score: `+X%` = 🟢 improving
- Detection Rate: `+X%` = 🟢 improving
- Sentiment: `+X` = 🟢 improving
- Mentions: `+X` = 🟢 increasing
- Citations: `+X` = 🟢 increasing
- Reputation Score: `+X` = 🟢 improving

### Position/Rank Metrics (lower is better)
- Avg. Position: `-X` = 🟢 improving (moved up)
- Avg. Position: `+X` = 🔴 declining (moved down)

---

## Example Complete Dashboard Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌟 Rankscale GEO Analytics Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Brand: HubSpot
Timeframe: Last 7 days
Last updated: 2026-02-26 18:52 GMT+1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIMARY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Visibility Score          🟢 ↑ +0.7
     69.1
  Out of 12 engines

🎯 Detection Rate            🟢 ↑ +2.1%
     79.2%
  Detected in 10 engines

😊 Sentiment                 🟢 ↑ +3
     74/100
  Positive brand mentions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOLUME METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Mentions                  🟢 ↑ +147
     2,189
  Across all engines

🔗 Citations                 🔴 ↓ -23
     4,057
  From external sources

📍 Avg. Position             🟢 ↑ -0.3
     #2.1
  Average ranking position

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPUTATION ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️  Reputation Score         🟢 ↑ +4.2
     85.2/100
  Strong positive perception

Risk Areas:
  • "Pricing can escalate" (3x)
  • "Steep learning curve" (2x)

Top Strengths:
  • "Marketing automation" (8x)
  • "Reliable platform" (6x)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Implementation Checklist

When implementing features, verify:

- [ ] Metric title matches exactly (e.g., "Visibility Score", not "Visibility")
- [ ] Trend indicator uses correct icon (↑ green, ↓ red, → gray)
- [ ] Main value has correct decimal places (visibility 1x, mentions 0x, etc.)
- [ ] Secondary text includes "out of", "across", "from", etc.
- [ ] Numbers are formatted (commas for counts >999, % for rates)
- [ ] Positive/negative interpretation matches metric type (position is inverse)
- [ ] No technical field names in output (no `ownBrandMetrics.`, no `sentiment.positiveKeywords`)
- [ ] Output respects 55-character width where possible
- [ ] Trend direction uses correct color coding
