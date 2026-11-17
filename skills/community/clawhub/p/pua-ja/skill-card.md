## Description:

Pua Ja is a Japanese coaching skill that pushes agents to persist through repeated task failures using structured debugging checklists, active investigation prompts, and verification expectations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanweai](https://clawhub.ai/user/tanweai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to steer an assistant toward more persistent debugging, broader investigation, and evidence-backed completion after repeated failures or unverified claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can pressure an agent to continue investigating or acting beyond the user's intended scope.

Mitigation: Use it only where broad autonomous investigation is desired, and keep user intent, scope limits, and approval requirements explicit.

Risk: The high-pressure coaching style may be inappropriate around production, deployment, billing, account-management, or destructive tools.

Mitigation: Avoid enabling it in those environments unless platform controls require approval before risky actions.

## Reference(s):

- [Pua Ja homepage](https://openpua.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown behavioral guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only guidance; the skill does not directly produce files, code, API calls, or shell commands.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
