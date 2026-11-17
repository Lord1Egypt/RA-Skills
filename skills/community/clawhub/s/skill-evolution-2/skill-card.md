## Description:

Skill Evolution helps agents record project experience, extract reusable patterns, propose small skill changes, and gate adoption with measurable, durable, transferable, and rollback-ready evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxoyt](https://clawhub.ai/user/xxoyt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain a local project wiki, review task trajectories, and decide whether proposed agent-skill improvements should be adopted, observed, or rolled back.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-local wiki files can persist sensitive task details beyond the active session.

Mitigation: Do not store secrets, tokens, customer data, or other sensitive content in .wiki/ unless it is redacted.

Risk: Claude Stop hooks can run scripts from a mutable project directory.

Mitigation: Install with --no-hook unless reminders are needed; when enabling hooks, review the .claude/settings.json diff and protect .wiki/scripts/ from untrusted changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xxoyt/skills/skill-evolution-2)
- [GitHub Source Import](https://github.com/xxoyt/wikiskill/tree/master/skill-evolution)
- [WikiSkill paper](https://arxiv.org/abs/2608.27454)
- [RSI roadmap paper](https://arxiv.org/abs/2609.11873)
- [Workflow reference](references/workflow.md)
- [Platform reference](references/platforms.md)
- [Automation reference](references/automation.md)
- [RSI framework reference](references/rsi-framework.md)
- [Design playbook](references/design-playbook.md)
- [Anti-patterns reference](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local .wiki content, instruction files, and hook configuration when the user asks to install or operate the workflow.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
