## Description: <br>
Captures agent learnings, errors, corrections, and missing capabilities in local markdown logs with anti-loop guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record corrections, command failures, missing capabilities, and external tool issues so future agent sessions can learn from them. It is intended for opt-in local learning workflows with explicit limits on repeated logging and promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs and promoted guidance can capture sensitive context or private operational details. <br>
Mitigation: Redact secrets, tokens, paths, environment variables, raw command output, and private user details before anything is written. <br>
Risk: Promotion into future agent guidance can change later agent behavior. <br>
Mitigation: Review every promotion into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions and keep promotion user-initiated. <br>
Risk: Broad hook configuration can inject reminders too often or in unintended workspaces. <br>
Mitigation: Keep hooks project-local and opt-in, and avoid empty or global matchers unless the workspace owner has explicitly accepted that behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/self-improving-agent-hardened) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown entries with shell and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append local .learnings entries and provide reminder text when configured through opt-in hooks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
