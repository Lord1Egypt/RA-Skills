## Description:

Enables agents to start a Vipshop QR-code login flow, show the QR code to the user, poll for confirmation, and save the resulting login cookies for other Vipshop skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viphgta](https://clawhub.ai/user/viphgta)

### License/Terms of Use:

MIT-0

## Use Case:

External users, agents, and developers use this skill to authenticate a Vipshop account by QR scan so downstream Vipshop skills can reuse the saved cookies for account-specific workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved Vipshop cookies in ~/.vipshop-user-login/tokens.json can be reused to access the user's account.

Mitigation: Keep the token file private, treat it like a password, and use logout or removal when the login state is no longer needed.

Risk: QR tokens or QR image URLs may appear in terminal output or logs during login.

Mitigation: Avoid sharing terminal logs or screenshots from login sessions, especially while a QR code is active.

Risk: Dependencies are declared without a reviewed lockfile.

Mitigation: Prefer pinned dependencies or a reviewed lockfile before installing in a controlled environment.

## Reference(s):

- [Vipshop QR Login API Reference](references/api_reference.md)
- [Vipshop QR Login Integration Guide](references/integration_guide.md)
- [Vipshop Login Skill Release Page](https://clawhub.ai/viphgta/skills/vipshop-user-login)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and text with CLI commands, Python snippets, machine-readable QR payload JSON, and a saved local JSON credential file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates ~/.vipshop-user-login/tokens.json with reusable Vipshop cookies after a successful login.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
