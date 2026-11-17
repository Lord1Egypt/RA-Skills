## Description:

Query public open data from Umeå kommun on locations, facilities, demographics, environment, infrastructure, and building permits with geospatial support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simskii](https://clawhub.ai/user/simskii)

### License/Terms of Use:


## Use Case:

External users, analysts, and developers use this skill to query Umeå kommun public open data for facilities, infrastructure, planning, demographics, and environmental questions, including nearby-location lookups when geospatial data is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Umeå municipality's public open-data API, so availability, rate limits, schema changes, or data freshness can affect answers.

Mitigation: Check important results against the source API and handle empty, stale, or failed responses before relying on outputs.

Risk: The nearest-location helper references a missing distance.jq file, which can cause nearby-location examples to fail.

Mitigation: Repair the package by adding the required distance.jq helper or avoid the nearby helper until packaging is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simskii/skills/umea-data)
- [Umeå Open Data API](https://opendata.umea.se/api/v2/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with Bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries public Umeå kommun open-data endpoints; nearest-location examples depend on the packaged distance.jq helper.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
