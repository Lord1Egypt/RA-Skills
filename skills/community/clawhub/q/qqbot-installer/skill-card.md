## Description:

OpenClaw QQ bot plugin installation and upgrade assistant that helps install or update openclaw-qqbot with file verification, rollback, and gateway restart support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install or upgrade the QQBot plugin, optionally pin a version, verify expected files, clean legacy plugin directories, and restart the gateway after installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent OpenClaw plugin installations and restart the gateway.

Mitigation: Review the exact command before execution, use a known QQBot package and plugin ID, and confirm restart timing with the operator.

Risk: The generic installer path and script handling are risky beyond a QQBot-only install.

Mitigation: Avoid passing untrusted package names, plugin IDs, or legacy directory names; prefer releases with allowlists, integrity checks, safer rollback, and explicit confirmation before restart or postinstall execution.

## Reference(s):

- [Qqbot Installer on ClawHub](https://clawhub.ai/ryanlee-gemini/skills/qqbot-installer)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plugin version and result summary lines when the installer script completes.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
