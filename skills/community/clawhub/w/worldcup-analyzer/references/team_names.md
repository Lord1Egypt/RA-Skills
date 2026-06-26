# Canonical team names (48 teams, 2026 FIFA World Cup)

> **Authoritative source: `GET /matches/teams/`.** Call `list_teams()` in
> `scripts/wc_client.py` (12h cached) instead of hardcoding the list below
> in any new code. The block here is a **fallback** for offline reasoning
> and a stable place to document aliases the API doesn't normalize itself.

When users provide a different spelling, normalize via
`canonicalize_team_name()` and then verify membership with
`validate_team(name, competition)` — that combo handles the alias map
plus a fuzzy "did you mean?" suggestion for typos.

## The 48 teams (snapshot, as of skill creation)

Algeria, Argentina, Australia, Austria, Belgium, Bosnia, Brazil, Canada,
Cape Verde, Colombia, Croatia, Curacao, Czech Republic, DR Congo, Ecuador,
Egypt, England, France, Germany, Ghana, Haiti, Iran, Iraq, Ivory Coast,
Japan, Jordan, Mexico, Morocco, Netherlands, New Zealand, Norway, Panama,
Paraguay, Portugal, Qatar, Saudi Arabia, Scotland, Senegal, South Africa,
South Korea, Spain, Sweden, Switzerland, Tunisia, Turkey, United States,
Uruguay, Uzbekistan.

## Common aliases

| Input (case-insensitive) | Canonical |
|---|---|
| 美国, 美利坚, USA, U.S., America | United States |
| 韩国, Korea Republic, Korea | South Korea |
| 科特迪瓦, Côte d'Ivoire, Cote d'Ivoire | Ivory Coast |
| 波黑, Bosnia and Herzegovina | Bosnia |
| 土耳其, Türkiye, Turkiye | Turkey |
| 库拉索, Curaçao | Curacao |
| 刚果民主共和国, 民主刚果, Congo DR, Democratic Republic of the Congo | DR Congo |
| 佛得角, Cape Verde Islands | Cape Verde |

Anything not in this list is passed through unchanged; the API will return
404 if it doesn't match.
