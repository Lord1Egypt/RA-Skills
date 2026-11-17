## Description:

Auto-healing and protection for OpenClaw workspaces that validates and repairs common startup and runtime issues such as missing memory files, invalid openclaw.json, HTTP provider URLs, missing API keys, and recurring LLM errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elontools](https://clawhub.ai/user/elontools)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep OpenClaw workspaces healthy by creating expected memory files, validating configuration, checking provider settings, and guiding recovery from common LLM and gateway failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic repairs can create files, edit configuration, restart services, or modify permissions in an OpenClaw workspace.

Mitigation: Require explicit user approval before changing openclaw.json, restarting services, or applying permission repairs.

Risk: The startup script can loosen Markdown file permissions with chmod 644.

Mitigation: Replace broad permission repair with least-privilege modes scoped to known safe workspace files.

Risk: Configuration fixes may affect provider connectivity or credentials.

Mitigation: Review proposed baseUrl and apiKey changes before applying them and keep a backup of openclaw.json.

## Reference(s):

- [Common Errors and Solutions](references/common-errors.md)
- [Health Checks](references/health-checks.md)
- [ClawHub Skill Page](https://clawhub.ai/elontools/skills/workspace-guardian)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and workspace file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace memory files, report configuration issues, and propose or perform maintenance actions in an OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
