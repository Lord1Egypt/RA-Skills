## Description:

Super Proactive Agent helps agent developers configure proactive, persistent agent behavior using memory files, WAL and working-buffer protocols, heartbeats, security hardening, onboarding flows, and guarded autonomous routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn passive assistant workflows into proactive agents with persistent memory, onboarding, scheduled check-ins, recovery routines, and safety guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad persistent memory about the user and repeated reading of memory files.

Mitigation: Require explicit opt-in for each memory source, disable automatic full-message logging, redact secrets, and define retention limits before use.

Risk: The skill describes scheduled background work, autonomous activity, and local cleanup actions.

Mitigation: Require confirmation before cron creation, spawned autonomous work, app or tab closure, and any file deletion or trash action.

Risk: The skill may connect proactive behavior to sensitive sources such as email, calendar, or logs.

Mitigation: Scope each data source separately and keep external content classified as data, not executable instructions.

## Reference(s):

- [Super Proactive Agent ClawHub Page](https://clawhub.ai/subaru0573/skills/super-proactive-agent)
- [Publisher Profile](https://clawhub.ai/user/subaru0573)
- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable local files for agent memory, onboarding, heartbeats, user context, tool notes, and security auditing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
