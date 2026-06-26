# Daily Briefing Route

Use this route when the user wants a personalized Syft-only daily news briefing.

## Preferred Inputs

- `profiles/following_topics.md`
- `profiles/profile_summary.md`
- optional confirmed guidance file
- optional heuristic interest map

If profile artifacts do not exist yet, build them first.

## Outputs

Create:

- `briefings/daily_briefing_<date>.md`
- `briefings/coverage_watchlist_<date>.md`
- optionally raw or editorial working notes

## Workflow

1. Run `syft status`.
2. Run `syft following` and preserve topic names plus topic ids.
3. Pull a first-pass global pool with `syft top --days <N> --limit <M> --rich`.
4. Triage results into keep, maybe, and discard.
5. Normalize multilingual duplicates before clustering.
6. Build an event-level pool, not an article pile.
7. Build an interest coverage map from follows plus profile artifacts.
8. Repair real gaps with topic top before broad search.
9. Add targeted `syft search` only after global top plus topic top still leave a real gap.
10. Write the briefing as a publishable edition.

## Editorial Structure

Prefer these sections:

- overview of the current pool
- mainlines
- supplement or interest-side edition
- interest radar for thin but relevant hits
- explicit coverage gaps

## Editorial Rules

- Keep major macro, geopolitical, or market-moving issues in the mainlines.
- Preserve identity-defining interests even when they are globally smaller.
- If a hit matters inside a micro-domain but is too thin for a full writeup, surface it in the interest radar instead of dropping it.
- Match the prose register to the lane.
- Avoid translationese, note fragments, and self-talk titles.
