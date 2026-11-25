## Description:

Checks an organization's historical forecast accuracy for the same series and horizon, including errors, bias, interval coverage, and notable misses, or reports when no coverage is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts use this skill to assess the historical reliability of forecasts from listed organizations such as the IMF, OECD, Federal Reserve, and public companies. It supports questions about forecast error, bias, interval coverage, and past misses for a matching series and horizon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious because its recommended MCP connection appears to expose Actor capabilities beyond forecast track-record analysis; the scan was partial.

Mitigation: Before installing, review which Actors the MCP connection exposes and whether inputs could reach unrelated Actors. Check unresolved package references because the security review was based on incomplete evidence.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/geminigeorge22/skills/publicrecords-forecast-track-record)
- [Calibration Ledger Actor on Apify Store](https://apify.com/publicrecords/calibration-ledger)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Forecast track-record analysis with source links, or an explicit no-coverage result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organization-level results only; beta coverage may not include every source, series, geography, or horizon.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
