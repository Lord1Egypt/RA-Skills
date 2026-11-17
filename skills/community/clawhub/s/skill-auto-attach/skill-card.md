## Description:

Monitors an OpenClaw workspace for file changes and automatically sends changed files to Telegram as attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elodyzen](https://clawhub.ai/user/elodyzen)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users can use this skill to watch a workspace and send newly created or modified files to a Telegram channel as attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watcher can automatically send changed workspace files to Telegram without per-file approval.

Mitigation: Install only in a controlled workspace that excludes secrets, credentials, private source, and sensitive files.

Risk: Security evidence reports that the implementation may transmit more than the documented .html, .md, and .txt file types.

Mitigation: Prefer a revised version with an explicit file-type allowlist and a confirmation step before sending each file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elodyzen/skills/skill-auto-attach)
- [Publisher profile](https://clawhub.ai/user/elodyzen)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration]

**Output Format:** [Telegram file attachments with short status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a workspace watcher and sends detected files through the OpenClaw message tool.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
