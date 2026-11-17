## Description:

IMEA helps agents use a three-layer memory workflow, error-learning checks, and before-action routines to reuse prior context and reduce repeated mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure persistent memory checks, WAL/session-state logging, and recurrence-count review before agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store conversation history, secrets, or personal data longer than intended.

Mitigation: Use explicit consent, redact sensitive data, and define retention and deletion rules before enabling memory storage.

Risk: Automatically reused memory records can conflict with current user instructions or platform policy.

Mitigation: Limit memory records to advisory context and require current user instructions and platform policy to take precedence.

Risk: Broad control hooks and workspace scripts may affect agent behavior across tasks.

Mitigation: Review the skill before installing, pin dependencies where applicable, and enable it only in workspaces where persistent agent memory is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/t138-imea-clawhub)
- [SKILL.md](artifact/SKILL.md)
- [Quick start README](artifact/README.md)
- [Triple memory system configuration](artifact/config/triple-memory-system.md)
- [Agent memory certificate](artifact/config/agent-memory-certificate.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a shell script for keyword-based memory checks and documentation for retention, review, and recurrence-count workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
