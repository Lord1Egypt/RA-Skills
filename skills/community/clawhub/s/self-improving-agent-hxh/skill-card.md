## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trumphuang](https://clawhub.ai/user/trumphuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, feature requests, and reusable lessons so future agent sessions can review or promote them into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files can capture sensitive conversation, error, or customer context. <br>
Mitigation: Record sanitized summaries only; do not log secrets, credentials, tokens, raw prompts, personal data, private URLs, full stack traces, or verbatim transcript content. <br>
Risk: Global hook activation can cause learning reminders or logging practices to spread across projects where persistent memory is inappropriate. <br>
Mitigation: Keep hooks project-scoped where possible and install the skill only in projects where durable learning memory has been reviewed and accepted. <br>
Risk: Promoting unreviewed learnings into always-loaded agent files can reinforce incorrect or overly broad guidance. <br>
Mitigation: Review and sanitize entries before promoting them into AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or similar prompt-context files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/trumphuang/self-improving-agent-hxh) <br>
- [Entry Examples](references/examples.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning files and prompt-context files when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
