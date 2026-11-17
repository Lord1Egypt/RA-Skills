## Description:

Cost-effective skill selector that evaluates local and ClawHub skills by quality, token cost, security and reliability, and speed before recommending options for user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binziai7996](https://clawhub.ai/user/binziai7996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to compare candidate skills, estimate execution cost, review security signals, and choose a suitable skill before installation or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend and install other skills, and server security evidence says its advertised security review may mark unverified packages as safe.

Mitigation: Independently inspect the exact package, publisher, requested permissions, and executable behavior before approving any recommended skill for installation.

Risk: Artifact behavior includes helper scripts that call ClawHub and OpenClaw commands and rely on placeholder parsing or scoring logic.

Mitigation: Treat rankings as decision support only; verify search results, score inputs, and security findings before acting on a recommendation.

## Reference(s):

- [Skill Evaluation Rubric](references/evaluation-rubric.md)
- [Security Audit Checklist](references/security-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/binziai7996/skills/skill-router-bzai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with ranked recommendations, scoring breakdowns, command examples, and JSON outputs from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated token use, execution time, cost, final scores, and security assessment summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
