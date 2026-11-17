## Description:

Sunday gives an agent its own email address and end-to-end encrypted credential vault for signups, logins, email verification, and stored credential workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:


## Use Case:

Developers and agents use Sunday when an agent needs a dedicated identity for service registration, credential storage and retrieval, login workflows, and read-only email verification without using a user's personal email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent receives long-lived autonomous access to decrypted passwords and OTP-capable email through an external CLI.

Mitigation: Use a dedicated low-risk Sunday identity, avoid personal or business-critical credentials, review the CLI publisher and update path before installation, and keep a revocation and credential-rotation path available.

Risk: The authenticated Sunday session stores credentials and encryption keys under the local Sunday configuration after login.

Mitigation: Use Sunday only on trusted agent hosts and revoke the session or rotate stored credentials if the host profile is exposed.

Risk: Passing secrets as command-line arguments can expose them through shell history or process listings.

Mitigation: Prefer generated passwords and avoid passing high-value secrets on the command line.

## Reference(s):

- [ClawHub Sunday Skill](https://clawhub.ai/raunaksingwi/skills/sunday)
- [Sunday Account Setup](https://sunday.ravi.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use --json where supported; Sunday inbox access is read-only and credential access depends on an authenticated Sunday CLI session.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
