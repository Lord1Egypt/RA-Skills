## Description:

Mandatory verification steps for all code reviews to reduce false positives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to make code review agents verify evidence before reporting findings, especially by reading the relevant code, checking references, considering mitigations, and calibrating severity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can narrow reviews and suppress newly discovered issues during re-review.

Mitigation: Install it only when this review posture is intended, and confirm that re-review scope restrictions match the team's review policy.

Risk: Mandatory review-output rules can over-constrain findings or treat advisory conventions as requirements.

Mitigation: Pair the protocol with local code-review policy and allow maintainers to override formatting or scope rules when they conflict with project requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance and review-checklist instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool, MCP, credential, or environment-variable outputs were identified in the artifact.]

## Skill Version(s):

1.0.20 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
