---
name: uberfix-branches
description: Find or list UberFix branches through its operational API.
---

# UberFix Branch Finder

Use this skill to list registered branches or locate nearby ones in the UberFix service network.

## Tools

- `uberfix_list_branches`: returns branches from the existing operational backend.
- `uberfix_find_nearest_branch`: use `latitude` and `longitude` in decimal degrees, optionally `city`; do not use `lat` or `lng` for the **operational** MCP endpoint.

Require the user's location or a named city before a nearby lookup. Distances returned by the backend are geographic estimates, not road travel time. Do not infer branch opening status or eligibility without supporting data. The operational backend's branch listing is not necessarily tenant scoped; use only properly limited credentials and never disclose another company's branch list without authorization.
