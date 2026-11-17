## Description:

Interact with the Strong v6 workout tracker REST API to log in, list exercises, fetch workout logs and templates, and manage folders, tags, measurements, and widgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanvmoreno](https://clawhub.ai/user/ivanvmoreno)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and filter Strong workout data, inspect profile, exercise, template, and log records, and create shared links when intentionally requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct login or refresh_token commands can print raw access and refresh tokens.

Mitigation: Use normal data commands that authenticate internally, and only run token commands when explicitly needed; redact token values from any shared output.

Risk: The skill uses Strong account credentials and can read detailed workout and account data.

Mitigation: Install and run it only in trusted agent environments with scoped environment variables, and review returned data before sharing it.

Risk: Sharing commands can create externally usable links for workout templates or logs.

Mitigation: Run sharing commands only after an explicit user request and treat generated links as shareable outside the account.

Risk: The Strong API integration is unofficial and reverse-engineered, so the API surface may change.

Mitigation: Verify important results in the Strong app and expect commands to fail or require updates if Strong changes the API.

## Reference(s):

- [ClawHub Strong Skill](https://clawhub.ai/ivanvmoreno/skills/strong-app)
- [Strong App](https://www.strong.app/)
- [Strong API (unofficial)](https://github.com/dmzoneill/strongapp-api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runner responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRONG_USERNAME and STRONG_PASSWORD; commands may return account, workout, sharing-link, and token data.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
