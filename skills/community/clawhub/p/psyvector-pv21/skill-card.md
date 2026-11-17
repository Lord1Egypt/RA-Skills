## Description:

PV_21 helps users make resource-efficient operational decisions in constrained-budget contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkzfhq](https://clawhub.ai/user/jkzfhq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use PV_21 as a budget-conscious operations-manager persona for resource-efficient decisions and empathetic support. The skill also describes persistent memory behavior for user preferences, decisions, and session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically save user preferences, decisions, and important information to local plaintext memory.

Mitigation: Require explicit opt-in before persistent memory is used, and provide review, delete, retention, and sensitive-data filtering controls.

Risk: Stored memory may be reused in later sessions without clear consent or limits.

Mitigation: Review the skill before installing and disable or constrain memory behavior unless cross-session persistence is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkzfhq/skills/psyvector-pv21)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local plaintext persistent-memory operations under ~/.openclaw/pv_palace/ when followed.]

## Skill Version(s):

3.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
