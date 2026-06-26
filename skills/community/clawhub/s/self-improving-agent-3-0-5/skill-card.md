## Description: <br>
Captures learnings, errors, corrections, and feature requests so coding agents can preserve and promote reusable knowledge across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mutsunico](https://clawhub.ai/user/mutsunico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to log corrections, command failures, missing capabilities, and reusable practices into local markdown learning files, then promote durable guidance into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived notes may persist sensitive or incorrect information in .learnings or promoted instruction files. <br>
Mitigation: Review and sanitize learning entries before promotion; do not store secrets, tokens, customer data, raw transcripts, or private error output. <br>
Risk: Optional hooks can add repeated reminders or inspect command output when configured globally. <br>
Mitigation: Enable hooks only after reviewing the scripts and choose minimal or project-scoped hook configuration when broad activation is not needed. <br>
Risk: Promoted guidance can influence future agent behavior without strong approval controls. <br>
Mitigation: Require manual review before moving learnings into persistent agent context files such as AGENTS.md, CLAUDE.md, TOOLS.md, or workspace memory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mutsunico/self-improving-agent-3-0-5) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning-entry templates, hook setup guidance, and skill extraction workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
