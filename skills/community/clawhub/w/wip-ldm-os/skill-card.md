## Description:

LDM OS installer and updater for installing, updating, checking status, and diagnosing LDM OS across supported agent harnesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

Dual License: MIT + AGPLv3

## Use Case:

Developers and agent operators use this skill to install, update, inspect, and repair LDM OS installations. It helps agents explain planned changes, run dry runs, and manage local identity, memory, hooks, MCP configuration, and shared workspace services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent changes to local agent harnesses, shell startup behavior, crontab entries, MCP configuration, hooks, and local message or context handling.

Mitigation: Review the dry run before running init or install commands, then use ldm doctor to inspect and repair the resulting configuration.

Risk: The release is flagged suspicious by the authoritative security evidence because it performs deep system-level agent management.

Mitigation: Install only when the operator intentionally wants LDM OS to manage multiple AI harnesses at that level.

Risk: Credential-backed integrations may depend on local secrets such as an OpenClaw service-account token.

Mitigation: Check whether ~/.openclaw/secrets/op-sa-token exists before enabling flows that require those integrations.

## Reference(s):

- [LDM OS Homepage](https://github.com/wipcomputer/wip-ldm-os)
- [LDM OS Install Document](https://wip.computer/install/wip-ldm-os.txt)
- [npm Package](https://www.npmjs.com/package/@wipcomputer/wip-ldm-os)
- [Technical Reference](TECHNICAL.md)
- [Universal Installer](docs/universal-installer/README.md)
- [Bridge](docs/bridge/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be presented with dry-run and consent checkpoints before installation changes are made.]

## Skill Version(s):

0.4.86 (source: release evidence, SKILL.md metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
