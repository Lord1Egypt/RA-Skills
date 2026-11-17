## Description:

Design or implement single-entry multi-agent routing for OpenClaw Weixin setups with configurable backend agents, per-agent session isolation, and summary-based handoff, reset, and status commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeqiulee](https://clawhub.ai/user/zeqiulee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or implement a Weixin plugin, extension, or reusable skill that routes one Weixin account to a configurable set of backend agents while keeping agent sessions isolated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous natural-language command matching could switch agents or reset context unintentionally.

Mitigation: Keep command matching explicit and conservative, and consider confirmation for reset actions before deployment.

Risk: Agent context could mix if a deployment uses a shared session instead of agent-scoped session identity.

Mitigation: Include the agent ID and session version in session keys, and validate that switching agents preserves separate memory.

Risk: Handoff behavior could expose more conversation history than intended.

Mitigation: Use compact summaries for handoff and avoid sharing raw transcripts between backend agents by default.

Risk: Public deployments could overfit commands to one locale or private alias set.

Mitigation: Document supported locales and aliases, keep agent maps configurable, and validate with at least two different agent maps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeqiulee/skills/weixin-multi-agent-router)
- [Architecture](references/architecture.md)
- [Commands](references/commands.md)
- [Configurability](references/configurability.md)
- [Validation](references/validation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON configuration examples, command patterns, validation checklists, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include router architecture, command maps, session-key guidance, handoff rules, reset behavior, and validation scenarios.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
