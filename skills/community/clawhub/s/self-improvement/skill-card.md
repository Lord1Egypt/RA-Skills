## Description: <br>
Captures learnings, errors, corrections, and feature requests so agents can record useful lessons and promote recurring patterns into project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike5230Odense](https://clawhub.ai/user/mike5230Odense) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to capture corrections, command failures, knowledge gaps, and feature requests as structured markdown logs. It also guides review and promotion of durable lessons into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture secrets, tokens, private prompts, customer data, or sensitive command output. <br>
Mitigation: Log short sanitized lessons only, exclude sensitive data, and keep learning files out of version control unless the team intentionally wants reviewed shared memory. <br>
Risk: Broad hook configurations can run reminders or inspect command output in more contexts than intended. <br>
Mitigation: Prefer project-level and narrowly matched hooks, review scripts before enabling them, and enable optional hooks only where the workflow needs them. <br>
Risk: Incorrect or outdated lessons can be promoted into persistent agent guidance. <br>
Mitigation: Review and scan entries before promotion, mark stale items resolved or superseded, and keep promoted rules concise and evidence-based. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with file templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings markdown logs, project memory files, hook configuration, or scaffolded skill files when directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
