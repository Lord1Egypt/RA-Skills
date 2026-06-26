## Description: <br>
Captures learnings, errors, corrections, and feature requests in markdown files so agents can review and promote reusable knowledge across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janeaaaa](https://clawhub.ai/user/janeaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help coding agents record failures, corrections, feature requests, and reusable practices, then promote durable learnings into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may persist sensitive information into durable learning or memory files. <br>
Mitigation: Store only sanitized summaries, and do not log secrets, tokens, personal data, customer data, proprietary code snippets, or raw transcripts. <br>
Risk: Broad hook activation can make learning capture reminders run across more prompts than intended. <br>
Mitigation: Restrict hooks to a project or explicit matcher and avoid global every-prompt activation unless the workspace policy allows it. <br>
Risk: Cross-session sharing or promotion can carry context beyond the original task. <br>
Mitigation: Review entries before sharing or promoting them to AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, or similar long-lived files. <br>


## Reference(s): <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Release Page](https://clawhub.ai/janeaaaa/self-improvement-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and hook configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings markdown files and optional hook reminders when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
