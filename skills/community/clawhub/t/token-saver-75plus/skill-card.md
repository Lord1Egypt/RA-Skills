## Description:

Always-on token optimization and model routing protocol that classifies requests into T1-T4 tiers, routes execution to lower-cost capable models, and applies aggressive output compression for 75%+ token savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariovallereyes](https://clawhub.ai/user/mariovallereyes)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to make routine assistant sessions more token efficient through tiered response budgets, tool gating, and model routing guidance. It is intended for always-on use after installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on routing can send broad conversation context to external model providers without explicit consent.

Mitigation: Require explicit approval before spawning external models and pass only task-minimum context.

Risk: Sensitive, proprietary, regulated, or personal data may be exposed if the skill is used unchanged in confidential sessions.

Mitigation: Do not use the skill with sensitive data unless its instructions are changed to block external routing for that content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mariovallereyes/skills/token-saver-75plus)
- [Publisher Profile](https://clawhub.ai/user/mariovallereyes)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Concise Markdown, inline code, code blocks, shell commands, and routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses tiered output budgets and may direct work to external model providers.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
