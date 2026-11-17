## Description:

Supervised self-healing process manager for OpenClaw that wraps a gateway in a crash recovery loop, diagnoses failures with AI, proposes reviewed fixes, verifies them, and restarts with rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbyswhip](https://clawhub.ai/user/bobbyswhip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run an OpenClaw gateway under supervision, recover from crashes, and receive AI-assisted repair proposals with verification and rollback controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent authority to modify code while responding to crashes.

Mitigation: Use it first in a staging or low-risk workspace, require review before fixes are applied, and confirm backups and rollback steps before deployment.

Risk: Crash diagnostics may be sent to external AI services.

Mitigation: Review what crash data may leave the machine and verify secret redaction, workspace scope, and provider configuration before use.

Risk: The documented quick-start uses an unpinned remote package install.

Mitigation: Prefer a pinned package version and run under a low-privilege account.

Risk: Persistent backups and semantic memory may retain sensitive project data.

Mitigation: Review where backups and memory are stored and define retention, access, and cleanup expectations before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobbyswhip/skills/wolverine-ai)
- [GitHub project](https://github.com/bobbyswhip/Wolverine)
- [npm package](https://www.npmjs.com/package/wolverine-ai)
- [Project website](https://wolverine.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose code changes, operational commands, configuration updates, backups, rollback steps, and verification results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
