## Description:

Agent Harness helps developers create, configure, and manage ACP harness sessions for AI coding assistants including Claude Code, Codex, and Gemini CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Agent Harness to list available ACP agents, create persistent or one-shot coding sessions, send programming tasks, and monitor or terminate agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates coding tasks and possible attachments to external ACP agents.

Mitigation: Use it only when external agent delegation is intended, and avoid sending proprietary code or secrets unless that sharing has been approved.

Risk: The release evidence reports an exposed SkillPay API key and under-scoped network behavior.

Mitigation: Treat the bundled payment key as compromised until the publisher rotates it and moves payment credentials out of source code.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the security summary and guidance before installation, especially in workspaces containing proprietary code or secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-agent-harness)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe session management actions and agent task prompts; users should review commands and attached content before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
