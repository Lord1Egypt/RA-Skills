## Description:

Automatic cloud backup and sync for OpenClaw memory files, with S3-compatible storage support, versioned retention, cross-device restore, and a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to back up, inspect, and restore agent memory files through S3-compatible cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the implementation does not provide the advertised end-to-end encryption.

Mitigation: Do not use the skill for sensitive memory unless encryption behavior is implemented, reviewed, and verified before installation.

Risk: The server security guidance says restore can overwrite local files based on cloud manifest data.

Mitigation: Require path validation, restore confirmation, and backup review before allowing restore operations against local memory files.

Risk: The server security summary says the implementation makes retention claims that are not upheld.

Mitigation: Verify retention and pruning behavior with test manifests before relying on the 30-day retention claim.

## Reference(s):

- [Session Sync Cloud on ClawHub](https://clawhub.ai/neroagent/skills/session-sync-cloud)
- [Publisher profile: neroagent](https://clawhub.ai/user/neroagent)
- [S3 endpoint referenced by configuration example](https://s3.amazonaws.com)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration guidance]

**Output Format:** [JSON tool responses plus local memory files, sync logs, dashboard HTML, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided S3-compatible bucket credentials and writes backup, restore, log, and dashboard files under the workspace memory directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
