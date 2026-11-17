## Description:

Parse pytest failure output into a prioritized fix plan with likely causes and minimal reproduction steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage failing pytest logs, prioritize likely causes, and plan focused checks and reruns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted CI logs may expose sensitive paths, environment details, or accidental secrets.

Mitigation: Redact confidential information before sharing pytest or CI output.

## Reference(s):

- [pytest documentation](https://docs.pytest.org/)
- [ClawHub skill release](https://clawhub.ai/hmahmadcs/skills/pytest-failure-triager)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with focused rerun commands and an action list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups failures, states assumptions, and gives a completion criterion.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
