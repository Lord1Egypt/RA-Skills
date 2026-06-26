---
name: srbijavoz
description: Check official Srbija Voz notices, station matches, and timetable metadata. Use when verifying live train delays, cancellations, stoppages, or replacement bus service in Serbia.
license: MIT
metadata: {"clawdbot":{"emoji":"🚆","requires":{"bins":["python3"]},"os":["linux","darwin"]}}
---

# Srbija Voz Status

Check official public Srbija Voz passenger-information endpoints and summarize whether a route has a live disruption, a timetable-only change, or no current issue.

## When to Use

- The user asks whether a Srbija Voz route currently has delays, cancellations, stoppages, or replacement bus service.
- The user wants current notices from the official Srbija Voz passenger-information site.
- The user needs station autocomplete matches from the timetable app.
- The user wants to confirm whether a notice is a live disruption or recurring timetable information.
- The user asks specifically about the Novi Sad - Petrovaradin corridor.

## Safe Scope

- Use only the official public passenger-information endpoints bundled in `scripts/srbvoz_scraper.py`.
- Treat this skill as read-only transit information lookup.
- Do not log in, solve challenges, bypass limits, or imitate protected user activity.
- If the public API stops working, use the timetable page fallback only for passive metadata checks.

## Check Current Notices

Run the bundled script first:

```bash
python3 scripts/srbvoz_scraper.py --limit 20
```

Filter notices when the user mentions a specific issue:

```bash
python3 scripts/srbvoz_scraper.py --query "kašnjenje" --limit 20
python3 scripts/srbvoz_scraper.py --query "Petrovaradin" --limit 20
```

The output JSON is the source of truth for current notices. Use notice title, content, date, and link in the final answer.

## Resolve Station Names

When the user gives a partial station name, call the station endpoint through the same script:

```bash
python3 scripts/srbvoz_scraper.py --station "Beograd"
```

Return the best matching station names and codes. Do not guess station names without checking the API first.

## Inspect Timetable Metadata

When the user asks whether something is a timetable artifact rather than a fresh notice, inspect the timetable page metadata:

```bash
python3 scripts/srbvoz_scraper.py --timetable-info
python3 scripts/srbvoz_scraper.py --station "Novi Sad" --timetable-info
```

Use this only to support interpretation. Prefer live notices over timetable-page hints.

## Classify the Result

Scan notice titles and bodies for disruption cues. Read `references/keyword-cues.md` when you need the full cue list.

Classify each relevant result as one of:

- `delay`
- `stopped`
- `canceled`
- `operational_change`
- `replacement_bus_service`
- `no_disruption_found`

On the Novi Sad - Petrovaradin corridor, treat recurring bus-service notices as timetable information unless the notice explicitly says service changed, stopped, or was canceled.

## Answer Format

Default to a short, rider-friendly summary.

Lead with the practical answer in plain language, for example:
- `No current issue found for Novi Sad -> Beograd.`
- `There is an issue on Novi Sad -> Beograd this morning.`
- `Only a recurring bus-transfer notice is present, no fresh disruption found.`

Then include only the useful operational details:
- whether there is a current issue or not
- affected route / train / departure times if known
- whether it looks current today, ongoing, or just a recurring timetable arrangement
- what the passenger should do, if obvious, for example use replacement bus, expect delay, or check the next departure

Do not include classifier jargon like `disruption type` unless the user asks for it.
Do not quote trigger phrases or explain the internal classification unless the user asks.
Mention `live notice` versus `recurring timetable notice` only when it helps disambiguate whether the issue is fresh.

If nothing relevant appears, say that no matching current notice was found.

## Handle Failures

- If the API request fails, the script can fall back to the public timetable page unless `--no-fallback` is set.
- If both API and fallback fail, say that the official public endpoints were unavailable at lookup time.
- If the user asks for exact timetable calculations, explain that this skill only checks public notices, station lookup, and timetable metadata.

## Tips

- Prefer route-specific queries like `Petrovaradin`, `Beograd centar`, or `Novi Sad` over generic searches.
- Quote the exact Serbian phrase that triggered the classification instead of paraphrasing the whole notice.
- A recurring bus notice on the Petrovaradin corridor is not enough by itself to claim a fresh disruption.
- Use `--station` before answering ambiguous station-name questions.
- Use `--timetable-info` only as supporting evidence, not as the primary source when live notices exist.
- Keep the final answer short and operational: what happened, where, and whether it appears current.
