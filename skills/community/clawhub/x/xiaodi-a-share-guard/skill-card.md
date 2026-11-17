## Description:

A Share Guard helps agents diagnose A-share stock risk using quote data, sentiment signals, and consensus-style risk scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx6315909](https://clawhub.ai/user/mx6315909)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to scan A-share stocks for valuation, technical, financial red-flag, and sentiment risks. It produces advisory risk reports and structured risk scores for review, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate unfinished financial-risk checks and make missing data look safe.

Mitigation: Treat pending, unavailable, or null financial indicators as incomplete evidence and require user review before relying on the final signal.

Risk: The release is intended for financial-risk analysis but is not dependable as investment advice.

Mitigation: Present outputs as informational risk screening only and require independent financial review before trading or portfolio decisions.

Risk: The bundled browserless configuration references a private-IP endpoint template.

Mitigation: Replace the template endpoint with an approved local or managed browserless service before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mx6315909/skills/xiaodi-a-share-guard)
- [Publisher profile](https://clawhub.ai/user/mx6315909)
- [Radar indicators](references/radar-indicators.md)
- [Configuration template](references/config-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown risk report with structured JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes stock code, timestamp, risk scores, red flags, sentiment/quant comparison, final signal, and advisory guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter, artifact metadata, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
