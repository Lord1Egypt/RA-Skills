## Description:

Reflection Replanner turns failed verification signals into categorized root-cause analysis and revised execution plans with remedial steps and a final verification gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill in long-running agent workflows to diagnose failed verification results, classify failure causes, and revise step-by-step plans instead of stopping after a failed check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local cross-session usage and preference memory that may affect future runs without clear consent, scoping, or retention controls.

Mitigation: Use the learner workflow only with reviewed, non-sensitive data; do not record secrets, personal data, customer data, or sensitive error payloads.

Risk: Learned patterns or proposed skill changes could introduce incorrect or misleading guidance into future executions.

Mitigation: Review learned_patterns.json and any proposed SKILL.md updates before relying on them or deploying the skill.

## Reference(s):

- [Reflection Replanner ClawHub page](https://clawhub.ai/qq435912743/skills/reflection-replanner)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON replanning outputs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local learned_patterns.json memory file when the learner workflow is used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
