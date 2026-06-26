## Description: <br>
Captures learnings, errors, and corrections so coding agents can preserve useful fixes and promote durable guidance across future sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangkang5](https://clawhub.ai/user/wangkang5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to log command failures, user corrections, missing capabilities, knowledge gaps, and recurring best practices into learning files that can be reviewed or promoted into persistent agent guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files may capture secrets, personal data, private prompts, or sensitive command output. <br>
Mitigation: Review entries before saving or promoting them, and do not store secrets, tokens, personal data, customer data, private prompts, or raw sensitive command output in learning files. <br>
Risk: Automatic hook reminders can add broad context across sessions and may be enabled too widely. <br>
Mitigation: Prefer project-local hooks, avoid empty matchers where possible, and review hook scripts before enabling them. <br>
Risk: Incorrect or stale learnings can be promoted into persistent agent instructions. <br>
Mitigation: Review and scan learnings before deployment, resolve stale entries, and promote only verified, broadly applicable guidance. <br>


## Reference(s): <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces learning-log entries, setup guidance, hook reminders, and skill-extraction guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
