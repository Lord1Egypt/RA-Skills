## Description:

CLI tool for Yandex Disk, Calendar, and Mail via Yandex OAuth API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smvlx](https://clawhub.ai/user/smvlx)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to authenticate with Yandex OAuth, inspect and move Yandex Disk files, list or create Yandex Calendar events, and report the documented Yandex Mail limitation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested OAuth scopes can include mail:smtp even though mail sending is not implemented.

Mitigation: Use the narrowest Yandex OAuth scopes needed for Disk and Calendar, and omit mail:smtp unless real mail sending is added.

Risk: The local Yandex OAuth environment file may contain secrets and is created without enforcing private file permissions.

Mitigation: Set ~/.openclaw/yax.env to mode 600 after setup and restrict access to the local user account.

Risk: Calendar event text is inserted into generated ICS content.

Mitigation: Avoid untrusted calendar summaries or descriptions until ICS escaping and validation are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smvlx/skills/yandex-cli-yax)
- [Publisher profile](https://clawhub.ai/user/smvlx)
- [Project homepage](https://github.com/smvlx/openclaw-ru-skills)
- [Yandex OAuth app registration](https://oauth.yandex.ru/client/new)
- [Yandex OAuth verification code](https://oauth.yandex.ru/verification_code)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [CLI text output and Markdown usage examples with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, a Yandex OAuth client ID, and local configuration under ~/.openclaw.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
