## Description:

1Password-backed credential filling via vault_suggest/vault_fill (plugin tools).

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to configure OpenClaw browser login workflows that fill credentials and TOTP values through 1Password-backed plugin tools while keeping secrets out of the agent transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A 1Password service-account token could be exposed if pasted into chat, committed, or stored in broadly readable environment files.

Mitigation: Prefer the 1Password desktop integration when possible; if a token is required, keep it out of chat, store it only in owner-only environment files, and rotate it if exposure is suspected.

Risk: Persistent gateway, systemd, sudo, or package-source changes can affect the user's local automation environment.

Mitigation: Manually approve gateway environment edits, systemd overrides or restarts, sudo commands, and Google Chrome package-source changes before applying them.

Risk: Autofill can place credentials into the wrong page or field if browser references are stale or misidentified.

Mitigation: Verify the page origin and field mapping before calling vault_fill, wait for filling to complete, and require user approval before submitting sensitive login forms.

## Reference(s):

- [Secure Autofill on ClawHub](https://clawhub.ai/moodykong/skills/secure-autofill)
- [OpenClaw project homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser-login workflow guidance and optional onboarding steps for local and gateway environment files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
