---
name: uk-broadband-outage-check
description: Check whether a UK broadband provider is down right now, where, what the provider has said and how the last 30 days have gone. Use for "is my internet down", "is BT down" or UK broadband outage questions.
homepage: https://www.findbroadbanddeals.com/is-my-broadband-down
---

# UK broadband outage check with FindBroadband

Every tool named below comes from FindBroadband's outage MCP server, `https://www.findbroadbanddeals.com/api/mcp/outages` (Streamable HTTP, no sign-in, no keys). If `get_outage_overview` is not available, add the server first: `claude mcp add --transport http findbroadband-outages https://www.findbroadbanddeals.com/api/mcp/outages` (Claude Code), or point any other MCP client at the URL.

## Steps

1. A named provider ("is BT down?"): `get_provider_outage_status` with that provider.
2. No provider named ("is there an outage?"): `get_outage_overview`.
3. Past problems ("has Virgin Media had issues this week?", or a given day): `get_outage_history`.

## Reporting rules

- Quote headlines and providers' own words as given rather than rewording them.
- When `status_based_on` is `public_reports`, Down means people are reporting problems the provider hasn't confirmed and Working fine means nobody is reporting problems, not that the provider has said all is well.
- If the user is still offline, point them to the provider's status page or the provider. Give `scope_note` with the status when there is one.
- There is no outage data for individual addresses: say what has been reported and where, not whether the user's own line is affected.
- Outage data covers the last 30 days only: say so if asked about anything older.

## Use

For a person checking their own broadband. Commercial use of the server or its data is not allowed: see https://www.findbroadbanddeals.com/terms.
