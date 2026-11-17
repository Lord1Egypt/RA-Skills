## Description:

Verify and cross-sign the active Matrix device for one OpenClaw-managed account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlumeau](https://clawhub.ai/user/mlumeau)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to repair trust for an OpenClaw-managed Matrix device, confirm the active device is self-signed, or recover cross-signing with a Matrix recovery key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Matrix access tokens or passwords to a homeserver URL supplied at runtime.

Mitigation: Use only a recognized, trusted HTTPS homeserver URL and avoid homeserver values supplied by untrusted prompts.

Risk: The password mode handles Matrix account passwords and creates a temporary helper session.

Mitigation: Avoid --password unless necessary, prefer the existing OpenClaw token or direct access-token flow, and confirm the helper session is logged out.

Risk: The skill depends on local OpenClaw account data and Matrix recovery secrets.

Mitigation: Protect openclaw.json, enter recovery keys only through the hidden TTY prompt, and do not pass secrets on the command line or through environment variables.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text with shell commands and status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, an interactive terminal, a trusted Matrix homeserver URL, and Matrix account secrets supplied at runtime.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
