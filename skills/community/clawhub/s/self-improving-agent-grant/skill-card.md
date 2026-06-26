## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwoodruff86](https://clawhub.ai/user/gwoodruff86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to capture corrections, command failures, API or tool issues, and recurring workflow improvements as markdown learning logs for later review or promotion to project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture sensitive project context if raw outputs, transcripts, secrets, tokens, or environment variables are copied into entries. <br>
Mitigation: Use project-local .learnings files by default, redact sensitive values, and summarize command output or transcripts instead of storing them verbatim. <br>
Risk: Always-on or user-level hooks can make learning reminders apply across unrelated workspaces and, when error detection is enabled, inspect command output for failure patterns. <br>
Mitigation: Prefer project-scoped hooks, keep hook setup opt-in, and enable command-output error detection only when that behavior is wanted for the workspace. <br>
Risk: Promoted learnings can influence future agents with stale, incorrect, or overly broad guidance. <br>
Mitigation: Review each learning before promoting it into files that future agents automatically read, and keep promoted guidance concise and scoped. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gwoodruff86/self-improving-agent-grant) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and reusable learning-entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports opt-in hook reminders and local markdown learning logs; users should review entries before promoting them into future agent context.] <br>

## Skill Version(s): <br>
3.0.16 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
