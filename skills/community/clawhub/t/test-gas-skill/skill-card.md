## Description:

Find and monitor gas prices with daily notifications. Use when searching for the cheapest gas in a specific area, tracking Costco and other discount fuel stations, or setting up daily gas price alerts. Supports any US location with configurable radius and fuel type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gustavoziaugra](https://clawhub.ai/user/gustavoziaugra)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search nearby US gas stations by ZIP code or coordinates, compare estimated Costco prices, and configure recurring gas price summaries.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can provide estimated or incomplete gas price information and may overstate monitoring, Costco, or coverage capabilities.

Mitigation: Treat results as estimates, verify prices with GasBuddy or station apps before acting, and review coverage expectations before deployment.

Risk: Location searches may be sent to external services, including a plaintext Overpass endpoint identified by the security scan.

Mitigation: Avoid sensitive locations, use HTTPS endpoints where possible, and review recurring alert schedules before enabling daily lookups.

Risk: Optional real-time GasBuddy behavior may require browser automation or commercial API access.

Mitigation: Use the default OpenStreetMap-based flow unless API credentials and browser automation dependencies have been reviewed and approved.

## Reference(s):

- [Gas Price Alert - US City Coordinates](references/locations.md)
- [Columbus, OH Area ZIP Codes](references/zip_codes.md)
- [Costco Warehouse Locations](https://www.costco.com/warehouse-locations)
- [GasBuddy](https://www.gasbuddy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON station results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print a human-readable summary to stdout or write station data to a JSON file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
