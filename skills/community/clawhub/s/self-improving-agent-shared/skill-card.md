## Description:

Captures agent learnings, errors, corrections, and feature requests so future sessions can review and promote durable guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorexxar](https://clawhub.ai/user/lorexxar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, missing capabilities, and recurring best practices in structured learning logs. They can then promote broadly useful entries into persistent agent guidance or extract reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and cross-session sharing can capture sensitive details if agents write raw transcripts, secrets, customer data, or file contents.

Mitigation: Store only sanitized summaries, and explicitly prohibit secrets, credentials, raw transcripts, customer data, and sensitive file contents in learning files.

Risk: Promotion into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or Copilot instructions can make incorrect or overbroad guidance persistent.

Mitigation: Require human approval before promoting learning entries into persistent prompt or instruction files.

Risk: Global hook activation can add reminders to every prompt and may create unwanted persistent-memory behavior.

Mitigation: Enable hooks only when the workspace needs them, prefer scoped or minimal hook configuration, and avoid global activation by default.

## Reference(s):

- [Self Improving Agent Shared on ClawHub](https://clawhub.ai/lorexxar/skills/self-improving-agent-shared)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and structured log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update learning logs, prompt files, hook configuration, and skill scaffolds.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
