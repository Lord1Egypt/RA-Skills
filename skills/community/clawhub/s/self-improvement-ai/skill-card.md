## Description: <br>
Captures learnings, errors, corrections, and feature requests so coding agents can document recurring issues and promote broadly useful guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fardeenkarim](https://clawhub.ai/user/fardeenkarim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to record command failures, user corrections, knowledge gaps, feature requests, and reusable practices in markdown learning logs. The skill also guides review and promotion of mature learnings into project or workspace memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture sensitive conversation, command, customer, token, or environment details. <br>
Mitigation: Keep logs project-scoped where possible, redact secrets and private transcript excerpts, and review entries before sharing or promotion. <br>
Risk: Promoting unreviewed entries into agent instruction files can introduce incorrect or misleading guidance. <br>
Mitigation: Review and validate learnings before promotion to AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions. <br>
Risk: Optional hooks can inject reminders and inspect command output, increasing context exposure if enabled too broadly. <br>
Mitigation: Enable hooks only when needed, prefer project-level configuration, and avoid logging raw command output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fardeenkarim/self-improvement-ai) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured log-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append or update local .learnings markdown files and project memory files when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
