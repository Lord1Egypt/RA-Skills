## Description:

Security agent that inventories installed OpenClaw skills, analyzes them for threats, and syncs results to your Clawned dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uttamnest](https://clawhub.ai/user/uttamnest)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to inventory installed skills, run explicit security scans, and sync security results to a Clawned dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sync and watch operations send installed-skill inventory and host registration metadata to a configurable Clawned server.

Mitigation: Install only if that data sharing is acceptable, keep CLAWNED_SERVER on the default HTTPS Clawned API unless you control the replacement endpoint, and avoid watch or scheduled sync when ongoing uploads are not desired.

Risk: Explicit scan submissions can send source file contents to Clawned, and symlinks in untrusted skill directories may cause out-of-scope local files to be read.

Mitigation: Scan only trusted skill directories, inspect scan targets for symlinks or sensitive files, and avoid scanning worktrees that contain private data.

## Reference(s):

- [Clawned homepage](https://clawned.io)
- [ClawHub skill page](https://clawhub.ai/uttamnest/skills/skill-sec)
- [Detection Patterns](references/detection-patterns.md)
- [Threat Model](references/threat-model.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text status and inventory output, JSON scan responses, and Markdown setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and CLAWNED_API_KEY; CLAWNED_SERVER is optional and defaults to the Clawned API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
