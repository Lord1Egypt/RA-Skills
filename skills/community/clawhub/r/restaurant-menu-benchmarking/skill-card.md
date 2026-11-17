## Description:

Compare restaurant menu breadth, matched dishes, bundles, and location-specific prices with the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant operators and analysts use the skill to compare branch-level menus, matched dishes, and prices across ordering channels and identify gaps in a defined market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark queries, restaurant identifiers, coordinates, and the API key are sent to Crawlora.

Mitigation: Use a service-scoped key and avoid sensitive unpublished business plans unless Crawlora is an approved vendor.

Risk: Repeated requests can consume API credits.

Mitigation: Bound queries to the requested scope and monitor credit usage.

Risk: Different branches, channels, bundles, or missing prices can produce misleading comparisons.

Mitigation: Verify branch and item matches, preserve missing prices, and distinguish menu prices from checkout totals.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/restaurant-menu-benchmarking)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Markdown comparison table and coverage summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes branch and source identifiers, collection times, match confidence, price differences, and missing-source coverage.]

## Skill Version(s):

1.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
