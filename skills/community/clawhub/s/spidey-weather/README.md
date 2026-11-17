# Spidey weather 1.0.0

Current conditions, today/tomorrow forecasts and a deterministic, spider-themed
outdoor-planning take. Defaults to Los Angeles; a city override lasts one call.
Works without the author's Google account, cloud deployment, router or Ollama.

## Requirements and installation

- Node.js 22 or newer (`node --version`). The helper uses Node's built-in fetch;
  there are **no npm dependencies or install scripts**.
- HTTPS access to `api.open-meteo.com` and `geocoding-api.open-meteo.com`.
- An OpenClaw host with either the existing project `weather_lookup` tool, or
  permission to execute the bundled Node helper. Skill installation alone does
  not register that tool or add permissions. Keep restricted host policies intact.

Install the complete released skill folder into a separate OpenClaw workspace's
`skills/spidey-weather/` directory. Start a fresh session and ask for
`$spidey-weather` with today's weather or a specific city. Do not copy only
`SKILL.md`: `scripts/` and `lib/` must travel with it.

After a public registry release exists, use its actual published slug/version:

```sh
clawhub install spidey-weather --version 1.0.0
```

The proposed slug is not a claim of public availability or name reservation.
The maintainer's publication record supplies the final link and version.

Manual use, from the installed skill folder:

```sh
node scripts/weather.mjs
node scripts/weather.mjs --location "Seattle, Washington" --country-code US
node scripts/weather.mjs --location "Tokyo, Japan" --country-code JP --day tomorrow
node scripts/weather.mjs --json
```

Output is Markdown by default; JSON includes `status`, `report`, and `weather`.
An ambiguous place returns choices instead of a guessed forecast. Exit status is
0 for a result or clarification, 1 for provider unavailability, and 2 for invalid
CLI arguments. Failed data is never presented as clear skies or zero rain.

## What is included

`SKILL.md` supplies agent instructions. `scripts/weather.mjs` is the helper.
Five `lib/*.mjs` files supply lookup, normalization, date formatting, icons and
readiness rules. Those modules are copied unchanged from the project's deployed
weather implementation by its package builder. No OpenClaw SDK import or private
profile is needed to execute them. The helper performs no model inference;
the assistant may use its configured model to interpret a request/select a tool.

## Readiness rules and limitations

The strongest applicable rule wins:

| Signal | Plan ahead | Use caution |
| --- | --- | --- |
| Forecast high; today's current temperature/feels-like | At least 90°F | At least 100°F |
| Forecast low; today's current temperature/feels-like | At most 45°F | At most 32°F |
| Forecast rain probability | At least 40% | No probability-only caution |
| Today's current wind | At least 15 mph | At least 25 mph |
| Reported weather condition | Rain/drizzle/snow/fog | Thunderstorm, freezing precipitation, heavy rain/snow, violent showers |

Mild complete readings receive Comfortable; unknown/missing inputs receive no
rating. Tomorrow excludes current conditions. These are authored product
heuristics, not official advisory thresholds or activity-specific safety advice.
The helper does not query official alerts, UV, air quality, gusts or tomorrow's
wind. Forecasts can be wrong; a rain probability is not a guarantee. Units are
Fahrenheit/mph; arbitrary dates and other units are not supported in this release.

## Data, attribution and privacy

Forecast and geocoding data: [Open-Meteo](https://open-meteo.com/), with
[forecast](https://open-meteo.com/en/docs) and
[geocoding](https://open-meteo.com/en/docs/geocoding-api) documentation.
Provider responses determine the resolved city, timezone and local dates.
Public API access is subject to [Open-Meteo terms](https://open-meteo.com/en/terms);
check those terms for your use case. No service availability is guaranteed.

Only the selected public city/region/country query and forecast parameters are
sent to the provider. Requests use fixed HTTPS origins, no redirects, a shared
15-second deadline, and a 128-KiB bound per response. The helper does not access
Gmail, Calendar, Tasks, credentials or retained chat, write user state, or create
scheduled jobs. It reads its own bundled program files as any Node program does.
Returned content remains untrusted data. This package is not proof of
prompt-injection resistance, and it does not sandbox its host process.

Project author: Aldo Caballero, CSCI 599 Assignment 3. Developed with AI assistance;
the project Process Log records authorship and integration. This is an independent
student project, not an official OpenClaw or Open-Meteo product or endorsement.
OpenClaw integration follows [Agent Skills](https://docs.openclaw.ai/tools/skills).

ClawHub releases skills under MIT-0, allowing reuse, modification and redistribution
including commercial use. The prepared local package has not yet been published;
the owner must review those registry terms before the public release. This note
does not change the license of the rest of the assignment repository or the
provider's data terms.
