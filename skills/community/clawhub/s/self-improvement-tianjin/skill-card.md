## Description: <br>
Captures learnings, errors, and corrections so agents can log failures, user corrections, missing capabilities, outdated knowledge, and better recurring-task approaches for future review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianjin-ren](https://clawhub.ai/user/tianjin-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to capture corrections, command failures, feature requests, and durable workflow learnings. They can then review those notes and promote recurring patterns into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning notes and promoted memory files can retain sensitive details such as tokens, credentials, customer data, private transcripts, or command output. <br>
Mitigation: Redact sensitive content before saving or promoting entries, keep .learnings local when appropriate, and avoid committing private logs. <br>
Risk: Broad hook configuration can repeatedly inject self-improvement reminders into future sessions. <br>
Mitigation: Enable hook-based reminders only when recurring reminder injection is wanted, and prefer the minimal activator-only setup for lower overhead. <br>


## Reference(s): <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Entry Examples](artifact/references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/tianjin-ren/self-improvement-tianjin) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with fenced shell, JSON, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .learnings files, hook reminders, and skill scaffold files when users choose those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
