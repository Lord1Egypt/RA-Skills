## Description: <br>
Captures learnings, errors, corrections, and feature requests in markdown files so agents can review and promote reusable knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgy7247](https://clawhub.ai/user/kgy7247) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agent operators use this skill to capture non-obvious errors, user corrections, feature requests, and reusable workflow lessons in project or OpenClaw memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived information may be written into .learnings or promoted memory files, exposing secrets or sensitive context if copied without review. <br>
Mitigation: Review and redact entries before storing or promoting them; do not store secrets, tokens, private transcripts, customer data, raw command outputs, or sensitive user details. <br>
Risk: Persistent hooks or broad workspace memory can cause agents to reuse stale, incorrect, or overgeneralized guidance. <br>
Mitigation: Keep hooks project-scoped where possible, inspect scripts before enabling them, and only promote learnings after they are reviewed and still applicable. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Learning Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, templates, and optional hook configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings files and optional agent hook configuration when applied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
