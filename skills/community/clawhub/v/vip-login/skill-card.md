## Description:

Provides a QR-code login flow for Vipshop accounts, showing a login QR code, polling for confirmation, and saving the resulting local session for other Vipshop skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authenticate a Vipshop account by scanning a QR code so agents and related Vipshop skills can make authenticated Vipshop requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable Vipshop login cookies on disk for later use by other skills.

Mitigation: Treat ~/.vipshop-user-login/tokens.json like an active login cookie, keep it on trusted machines only, and use logout or file removal when access is no longer needed.

Risk: Saved cookies can be reused across related local Vipshop skills with limited scoping controls.

Mitigation: Install and run only trusted Vipshop skills that require this session, and review which skills can read the local token directory.

Risk: Python dependencies are declared with lower-bound versions rather than fully pinned versions.

Mitigation: Install dependencies in an isolated environment with pinned or reviewed package versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vip-login)
- [Vipshop QR login API reference](artifact/references/api_reference.md)
- [Vipshop login integration guide](artifact/references/integration_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command and JSON snippets; scripts can emit machine-readable JSON markers for QR image display.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and reuses a local Vipshop login session file for downstream Vipshop skills.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
