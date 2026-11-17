## Description:

Manage and monitor remote GPU servers over SSH with GPU, disk, process status, alerts, log tailing, file sync, and health diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderfga](https://clawhub.ai/user/enderfga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ssh-lab to inspect GPU server health, run remote commands, tail logs, sync files, compare hosts, and manage alerts across SSH-accessible servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A host-alias command-injection issue in src/ssh/config.ts can run local shell commands when untrusted host names are used.

Mitigation: Install only after review, use trusted host names and prompts, and avoid untrusted host aliases.

Risk: High-impact SSH operations such as run, sync, watch, tail, and all-host commands are broadly scoped.

Mitigation: Require explicit approval before high-impact operations, prefer dry-run for sync, and pin the package version instead of using unpinned npx.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderfga/skills/ssh-lab)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Human-readable summaries, structured JSON, raw CLI output, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports summary, json, raw, heartbeat, and quiet output modes; results may include live SSH and rsync command output.]

## Skill Version(s):

0.1.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
