## Description: <br>
Captures errors, corrections, and recurring patterns into structured `.learnings/` logs, then promotes durable guidance into workspace memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollieb89](https://clawhub.ai/user/ollieb89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture actionable corrections, command failures, capability gaps, and recurring patterns so future sessions can reuse or promote them into workspace guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning guidance can affect many future sessions and projects if installed globally. <br>
Mitigation: Prefer project-local setup, review hook configuration before enabling it, and avoid global hooks unless broad persistence is intentional. <br>
Risk: Prompt, tool output, errors, credentials, personal data, or proprietary code could be saved into durable memory files if captured without review. <br>
Mitigation: Require explicit approval before saving sensitive content, and review `.learnings/` entries before promoting them into workspace memory files. <br>
Risk: Generated skill scaffolds may include incomplete placeholder content. <br>
Mitigation: Use dry-run mode first and require human review before treating extracted skills as reusable guidance. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/ollieb89/self-improving-agent-ollieb89) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace learning logs and skill scaffolds when users choose to apply its guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
