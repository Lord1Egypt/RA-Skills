## Description:

Analyzes individual retail clerk performance using POS data and, for AIoT stores, additional customer-funnel and trial-conversion data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail managers and store operations analysts use this skill to evaluate a single clerk's sales performance, product mix, order structure, AIoT conversion behavior, trends, findings, and coaching recommendations for a specified store and date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles employee-level performance data.

Mitigation: Limit execution to authorized managers or analysts and require explicit store, clerk, and date parameters for each analysis.

Risk: The security review reports that code is loaded from a hard-coded external folder.

Mitigation: Confirm the API client is packaged or imported from a trusted, controlled location and remove the developer-local path override before production installation.

Risk: AIoT customer-funnel data can be incomplete when clerk badge or profile data is missing.

Mitigation: Review generated notes and warnings before using AIoT findings for coaching or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-clerk-performance-analysis)
- [Skill definition](artifact/SKILL.md)
- [Usage guide](artifact/USAGE.md)

## Skill Output:

**Output Type(s):** [analysis, json, guidance]

**Output Format:** [Structured JSON-style analysis with findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit store ID, clerk name, start date, and end date; AIoT sections are included only when relevant store data is available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
