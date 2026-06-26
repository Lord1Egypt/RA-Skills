# Surf Region Ranking Skill

Use this skill when the user asks for the best surf spots in a region based on wave height, wind direction, and wind speed.

## Goal

For a user-specified region:

1. Run the surfline_region_report.py script to gather surf, wind, and tide data per spot in the specified region.
2. Score every spot in the region inside the agent (not in Go).
3. Return the top 3 spots by total score with explanations of their grades.

Category scores are:

- Wave height `/10`
- Wind direction `/10`
- Wind speed `/10`

Total score is `/30`.

## Important architecture rule

The Python script is **data collection only**.  
It must not be treated as a scorer or ranker.

- Script responsibility: fetch and output spot data
- Agent responsibility: score spots and choose top 3

## Required script command

Preferred (preset regions):

- `python3 surfline_region_report.py --region <region> --hours <hours> --output json`

Custom spot IDs:

- `python3 surfline_region_report.py --spots "<spotId1,spotId2,...>" --hours <hours> --output json`

Default `hours` to `24` unless the user asks otherwise.

## Regions supported by preset

- `north-orange-county`
- `south-orange-county`
- `san-diego`
- `santa-cruz`

If the user gives an unsupported region, ask for Surfline spot IDs for that region.

## Parse JSON output from the script

Read `spots[]` from script output. Each spot includes:

- `spotId`
- `avgSurfMinFt`
- `avgSurfMaxFt`
- `avgPrimarySwellFt`
- `avgWindMph`
- `avgWindDirectionDeg`
- `avgTideFt`
- `validHours`

Use `avgSurfMaxFt` as the main wave-height comparison value.

## Scoring rubric (agent-side, 0-10 each)

Compute scores for all valid spots in the selected region.

### 1) Wave height score (0-10, relative within region)

Let `waveMax = avgSurfMaxFt`.

- `waveScore = 10 * (waveMax - minWaveMax) / (maxWaveMax - minWaveMax)`
- If all spots have identical `waveMax`, assign `waveScore = 5` for all
- Clamp to `[0, 10]`

Interpretation: bigger rideable waves in the same region score higher.

### 2) Wind speed score (0-10, lower is better)

Let `windSpeed = avgWindMph`.

- `<= 4 mph`: `10`
- `> 4 and <= 8`: `8`
- `> 8 and <= 12`: `6`
- `> 12 and <= 16`: `4`
- `> 16 and <= 20`: `2`
- `> 20`: `0`

### 3) Wind direction score (0-10)

Default directional rubric unless user provides local break orientation:

- `315-360` or `0-45`: offshore/cross-offshore -> `9`
- `46-90` or `271-314`: side-shore -> `6`
- `91-270`: onshore/cross-onshore -> `2`

If user provides local direction guidance for a break, that guidance overrides defaults.

## Total score

- `totalScore = waveScore + windSpeedScore + windDirectionScore`
- Max total = `30`
- Round all category and total scores to 1 decimal place

## Required response format

Return only the top 3 spots sorted by `totalScore` descending.

For each ranked spot include:

- Spot ID (or spot name if available)
- Wave score `/10` and `avgSurfMaxFt`
- Wind direction score `/10` and `avgWindDirectionDeg` plus label
- Wind speed score `/10` and `avgWindMph`
- Total score `/30`
- 1-3 sentence explanation of why the spot earned the rank

After the list, include one short sentence naming the #1 recommendation.

## Behavior rules

- Always score all valid spots before picking top 3.
- If fewer than 3 valid spots exist, return all and explain why.
- If script fetch fails for a spot, exclude it and mention exclusion.
- Do not invent missing values; only use data returned by the script.
