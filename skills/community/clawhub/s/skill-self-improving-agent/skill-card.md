## Description: <br>
Captures learnings, errors, feature requests, and corrections so coding agents can preserve and promote useful lessons across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincntk](https://clawhub.ai/user/vincntk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to log failed commands, user corrections, feature requests, and reusable lessons into local markdown records. The skill also guides promotion of broadly useful lessons into agent memory or project instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can retain secrets, tokens, customer data, private paths, raw transcripts, or full command outputs. <br>
Mitigation: Redact sensitive data before logging, prefer summarized entries, and keep `.learnings/` out of version control unless intentionally shared. <br>
Risk: Promoting entries to memory files or sharing them across sessions can spread private or inaccurate guidance. <br>
Mitigation: Require explicit review and approval before promotion or cross-session sharing. <br>
Risk: Optional hooks can inject reminders or inspect command results during agent workflows. <br>
Mitigation: Keep hooks opt-in, inspect hook scripts and configuration before enabling them, and use them only in trusted workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincntk/skill-self-improving-agent) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration Guide](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning logs and optional hook setup guidance; no structured machine-readable output is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
