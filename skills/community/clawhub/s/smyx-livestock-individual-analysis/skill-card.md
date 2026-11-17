## Description:

Identifies individual pigs, cattle, and sheep from face or body-pattern images or videos and returns an individual ID with confidence for farm tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Farm operators and developers use this skill to identify individual livestock from images or videos, retrieve identification reports, and associate records with an animal ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Livestock media and report-history requests are sent to configured lifeemergence.com services.

Mitigation: Review the service destination before use and confirm history lookups explicitly.

Risk: The skill creates or reuses a local identity and persists service tokens, which may expose farm records on shared machines.

Mitigation: Restrict access to the workspace and review or clear its local data database on shared devices.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-livestock-individual-analysis)
- [Skill API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured identification results and Markdown report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes individual IDs, confidence values, matching features, and report links when available.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
