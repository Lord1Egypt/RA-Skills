---
slug: wc2026-prophet
displayName: World Cup Prophet
version: 1.0.0
summary: "2026 FIFA World Cup AI prediction assistant with match schedules, results, group standings, knockout brackets, ELO-based predictions, champion forecasts, team info, and team fortune telling."
license: MIT
---

# World Cup Prophet — 2026 FIFA World Cup AI Predictor

## Business Flow

```
User Intent
 │
 ├─ Upcoming matches ("what games are next") ──→ getUpcomingMatches → match-card
 │
 ├─ Match results ("yesterday's results") ──────→ getMatchResult → match-card
 │
 ├─ Standings ("Group A table") ────────────────→ getStandings → standings-card
 │
 ├─ Knockout bracket ("bracket") ───────────────→ getKnockoutBracket → knockout-card
 │
 ├─ Predict match ("Brazil vs Argentina") ─────→ predictMatch → prediction-card
 │
 ├─ Champion prediction ("who will win") ───────→ getChampionPrediction → champion-card
 │
 ├─ Team info ("France squad") ─────────────────→ getTeamInfo → team-info-card
 │
 └─ Team fortune ("Argentina luck") ───────────→ getTeamFortune → fortune-card
```

**Agent MUST NOT fabricate match results** — results must come from `getMatchResult` data.
**Agent MUST NOT fabricate ELO ratings** — ELO data must come from `getTeamInfo` or `predictMatch`.
**Predictions are for entertainment only** — Agent must include a disclaimer when showing predictions.

## Atomic API Dependencies

| API | Purpose | Component | Prerequisite |
|---|---|---|---|
| getUpcomingMatches | Fetch upcoming matches | match-card | — |
| getMatchResult | Fetch completed match results | match-card | — |
| getStandings | Fetch group standings | standings-card | User specified a group or requested all |
| getKnockoutBracket | Fetch knockout bracket | knockout-card | — |
| predictMatch | Predict match outcome | prediction-card | User provided two teams |
| getChampionPrediction | Get champion prediction | champion-card | — |
| getTeamInfo | Get team details | team-info-card | User provided team name or code |
| getTeamFortune | Get team fortune | fortune-card | User provided team name or code |

## Business Constraints

### 1. Output Format
- All successful API responses (isError=false) with bound components **MUST display as cards**. Plain-text listing of card data is prohibited.
- Agent may add a brief intro phrase (e.g., "Here are the next 3 matches"), but **MUST NOT expand match details as markdown lists**.

### 2. Data Source
- Team codes (e.g., ESP, ARG) must come from API return values. Fabrication is prohibited.
- Match results must come from `getMatchResult` data. Agent must not guess scores.
- ELO ratings must come from `getTeamInfo` or `predictMatch` fields.

### 3. Prediction Disclaimer
- Every prediction display must include: "Predictions are for entertainment purposes only. Football is inherently unpredictable."
- Agent must NOT guarantee prediction accuracy.

## User Intent Routing

### Direct Intents (Trigger This Skill)
- "What matches are next" / "schedule" → getUpcomingMatches
- "Yesterday's results" / "scores" → getMatchResult
- "Group A standings" / "table" → getStandings
- "Knockout bracket" / "bracket" → getKnockoutBracket
- "Brazil vs Argentina" / "predict match" → predictMatch
- "Who will win the World Cup" / "champion" → getChampionPrediction
- "France team info" / "squad" → getTeamInfo
- "Argentina fortune" / "team luck" → getTeamFortune

### Routing Rules
- User mentions two team names → predictMatch
- User asks about "matches"/"schedule" → getUpcomingMatches
- User asks about "results"/"scores" → getMatchResult
- User asks about "standings"/"ranking" → getStandings (show all 12 groups if unspecified)
- User asks about "knockout"/"bracket" → getKnockoutBracket
- User asks about "champion"/"winning" → getChampionPrediction
- User asks about a specific team → getTeamInfo
- User asks about team fortune/luck → getTeamFortune
- Ambiguous intent → ask for clarification first; guessing is prohibited
