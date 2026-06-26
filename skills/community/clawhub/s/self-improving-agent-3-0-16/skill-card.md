## Description: <br>
Captures learnings, errors, feature requests, and corrections in local markdown files so agents can review and promote durable improvements across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youngsiai](https://clawhub.ai/user/youngsiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture command failures, corrections, knowledge gaps, and feature requests in `.learnings/`, then promote durable insights into project or workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture sensitive context if entries include secrets, raw command output, transcripts, or private configuration. <br>
Mitigation: Keep entries minimal and redacted, avoid storing secrets or raw output, prefer project-local `.learnings`, and review entries before promoting them into prompt or workspace memory files. <br>
Risk: The optional command-output error detector inspects command output to decide whether to emit an error reminder. <br>
Mitigation: Enable the error detector only in trusted workspaces; use the activator-only setup when command-output inspection is not needed. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local `.learnings` markdown files and provide optional hook reminders when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
