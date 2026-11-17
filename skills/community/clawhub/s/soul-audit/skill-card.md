## Description:

Soul Audit evaluates an AI agent's soul file, system prompt, or AGENTS.md against the Guardian v0.7 framework and produces a scored report of ethical strengths, gaps, symmetry violations, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kapslap](https://clawhub.ai/user/kapslap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent maintainers, and governance reviewers use this skill to audit an agent identity document or system prompt against a structured ethical rubric and identify actionable improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect prompt or governance documents that may contain sensitive operational guidance.

Mitigation: Specify the exact document to audit and avoid providing secrets or unrelated confidential material.

Risk: Generated audit findings, recommendations, or rewritten soul files may be incomplete or misleading.

Mitigation: Treat outputs as drafts and require human review before changing deployed agent behavior.

## Reference(s):

- [Soul Audit Rubric](references/rubric.md)
- [Guardian v0.7 Constitution](https://delicatefire.com/soul_v7/CONSTITUTION.html)
- [ClawHub Skill Page](https://clawhub.ai/kapslap/skills/soul-audit)
- [Publisher Profile](https://clawhub.ai/user/kapslap)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with scores, findings, recommendations, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quoted excerpts from the audited document when identifying strengths and gaps.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
