## Description: <br>
Captures learnings, errors, corrections, feature requests, and recurring patterns so coding agents can document and promote useful project knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardan01](https://clawhub.ai/user/richardan01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture task learnings, command failures, user corrections, missing capabilities, and reusable patterns in markdown logs. It can also provide optional hook-based reminders and extraction guidance for promoting recurring learnings into durable agent instructions or new skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files and promoted instruction files can capture sensitive or private context if users log raw transcripts, secrets, tokens, customer data, private paths, or command output. <br>
Mitigation: Review entries before writing or promotion, redact sensitive data, and keep learning scope to project-level files unless broader sharing is intentional. <br>
Risk: Optional always-on hooks can inject reminders across many sessions and may increase unwanted persistence or prompt noise if enabled globally. <br>
Mitigation: Prefer project-level hook setup, narrow matchers where possible, and review hook scripts before enabling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richardan01/selfimproving) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [Hook Setup Guide](artifact/references/hooks-setup.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, templates, and hook configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append persistent learning entries and optionally emit hook reminders when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
