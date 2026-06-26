## Description: <br>
Captures learnings, errors, and corrections so an agent can record failures, user corrections, missing capabilities, outdated knowledge, and reusable improvements for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivercagropecuaria-cyber](https://clawhub.ai/user/drivercagropecuaria-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture operational learnings, command failures, user corrections, and feature requests in structured markdown logs. It also guides review and promotion of durable lessons into agent memory or project instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived context, including sensitive prompts, credentials, customer data, or personal details, into local learning files. <br>
Mitigation: Keep logs local where possible and redact secrets, credentials, private prompts, customer data, and personal details before writing entries. <br>
Risk: Promoted learnings can change future agent behavior through AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions. <br>
Mitigation: Manually review any learning before promoting it into persistent agent or project instruction files. <br>
Risk: Global hooks can run reminders across projects and increase unwanted persistence of cross-project context. <br>
Mitigation: Avoid global hooks unless that behavior is intended; prefer project-scoped activation and verify the package slug and source before installation. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/drivercagropecuaria-cyber/self-improving-agent-orbit) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable logging guidance, setup snippets, and templates for learning, error, and feature-request records.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
