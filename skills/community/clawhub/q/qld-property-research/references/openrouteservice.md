# openrouteservice Routing

## Contents

- Purpose
- API key setup
- Endpoint and auth
- Skill usage
- Attribution and caveats

## Purpose

Use openrouteservice only for the walking route to the nearest train station. Keep flood and main-road proximity on official Queensland or council data sources.

This is an explicit exception to the skill's normal official-source policy because public official routing data is not strong enough for walk-path extraction.

## API key setup

Store the key in an environment variable before running the skill:

```sh
export ORS_API_KEY='your-key-here'
```

The helper script also accepts `OPENROUTESERVICE_API_KEY`, but `ORS_API_KEY` is the preferred name.

If you want the key available in future terminal sessions, add the export line to your shell profile and restart the agent session so the new environment is inherited.

Do not hard-code the key in `SKILL.md`, scripts, or checked-in files.

## Endpoint and auth

Use the public directions API:

- Base API: [openrouteservice API](https://api.openrouteservice.org/)
- Directions request and return types: [Directions requests and return types](https://giscience.github.io/openrouteservice/api-reference/endpoints/directions/requests-and-return-types)
- Restrictions: [API restrictions](https://openrouteservice.org/restrictions/)

Use:

- `POST /v2/directions/foot-walking/geojson`

Send the API key in the `Authorization` header. The public docs describe the directions endpoint variants; the interactive API and HeiGIT examples use the key as plain header content rather than a Bearer token.

## Skill usage

1. Resolve the property coordinates from an official Queensland or council source.
2. Resolve the nearest station from official Translink or Queensland Rail sources.
3. Use `scripts/ors_walk_route.py` with the property and station coordinates.
4. Use the returned route distance and duration as the base walking evidence.
5. Add the fixed major-road crossing penalty from [methodology.md](methodology.md).
6. Cite the route as third-party walking analysis in the report.

If the script returns `status: not_configured`, keep the train section partial and explicitly say that openrouteservice is not configured in the current environment.

The helper script returns:

- `status: not_configured` when the API key is missing
- route distance in metres
- route duration in seconds
- turn-by-turn step count
- GeoJSON geometry and summary fields from ORS

## Attribution and caveats

When using free openrouteservice APIs, include attribution in the report source list or nearby note:

`© openrouteservice.org by HeiGIT | Map data © OpenStreetMap contributors`

Relevant docs:

- [Terms of Service](https://openrouteservice.org/terms-of-service/)
- [FAQ on API keys and server-side use](https://giscience.github.io/openrouteservice/frequently-asked-questions)

Keep these caveats:

- openrouteservice routing is third-party and OSM-based, not an official government walking route.
- Use it only to support station-access estimation, not flood or road classification.
- Keep the API key server-side or in the local runtime environment; do not expose it in user-facing output.
