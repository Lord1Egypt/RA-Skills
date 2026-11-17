## Description:

Retrieves Chinese transportation standards (GB, JT, and GA) through the Solvex API and formats citations for smart transportation proposals and technical documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solvex-top](https://clawhub.ai/user/solvex-top)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and transportation solution teams use this skill to query relevant Chinese GB/JT/GA standards and insert formatted citations into smart transportation proposals, bids, and technical plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Standards lookup queries are sent to a third-party API.

Mitigation: Use minimal generic keywords and avoid sending customer names, exact locations, bid details, unpublished architecture, credentials, or full proposal text.

Risk: Broad global installation and update-to-latest instructions can expand the skill's reach before review.

Mitigation: Prefer project-local installation and review the skill before updating or deploying it broadly.

Risk: Long-lived API keys in agent-wide settings can increase exposure if reused across projects.

Mitigation: Use the narrowest available secret mechanism and avoid storing long-lived API keys in global agent settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solvex-top/skills/traffic-standards-kb)
- [Solvex API service](https://solvexpert.net)
- [Solvex standards query endpoint](https://solvexpert.net/api/v1/standards/query)
- [API reference](artifact/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, API request examples, JSON response examples, and formatted standards citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Solvex API key and sends standards lookup queries to solvexpert.net.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
