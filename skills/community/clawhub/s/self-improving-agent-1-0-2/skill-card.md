## Description:

Captures learnings, errors, and corrections to enable continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[txmerlxn](https://clawhub.ai/user/txmerlxn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, feature requests, and knowledge gaps in structured learning logs, then promote durable lessons into project or agent memory when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable learning notes may capture sensitive conversation details or raw command output.

Mitigation: Keep .learnings/ local by default, redact secrets and raw command output, and review entries before sharing or committing them.

Risk: Promoting learnings into persistent instruction files can alter future agent behavior.

Mitigation: Require explicit approval before modifying CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Cross-session history or message sharing can expose context beyond the current task.

Mitigation: Do not use cross-session history or message sending without consent and redaction.

Risk: Global every-prompt hooks can add persistent reminders and inspect command output paths.

Mitigation: Avoid global hooks unless scripts and paths have been reviewed; prefer opt-in project-level setup.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [Clawdbot Integration Guide](references/clawdbot-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .learnings/ files and, with explicit approval, project or agent instruction files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
