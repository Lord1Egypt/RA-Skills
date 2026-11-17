## Description:

Create and manage short URLs with custom aliases and tracking, including QR-code generation for URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create local URL aliases, manage custom short codes, list saved URLs, inspect simulated click counts, and generate QR-code image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret-bearing URLs may be stored locally if users shorten password-reset links, signed URLs, API-token URLs, or similar sensitive links.

Mitigation: Use the skill only for non-sensitive URLs and avoid storing links that contain credentials, tokens, or private access grants.

Risk: URL aliases and metadata are written to local JSON storage in the user's home directory.

Mitigation: Treat the local data file as user data, review it before sharing environments, and remove entries that should not persist.

Risk: QR-code generation depends on an optional package install suggestion.

Mitigation: Pin and review the QR dependency before installing it in sensitive or managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/url-shortener)
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON storage in the user's home directory and PNG files when QR-code generation is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
