## Description:

Monitor library book availability and get notified when books become available for borrowing. Supports Shenzhen Library and extensible for other libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yszheda](https://clawhub.ai/user/yszheda)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to track book availability at Shenzhen Library, manage a monitored book list, and receive notifications when matching books become available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell commands, read and write local files, and contact Shenzhen Library.

Mitigation: Review the requested command and configuration before execution, run it in an appropriate workspace, and use reasonable monitoring intervals.

Risk: Email notifications can expose book-interest data and may require SMTP credentials.

Mitigation: Use a dedicated app password, limit recipients, or remove email from notification methods when email alerts are not needed.

Risk: Notification configuration may still initialize email behavior when email remains configured.

Mitigation: Remove email configuration or inspect notification settings before relying on notification.enabled as the only control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yszheda/skills/skill-openclaw-library-monitor)
- [Shenzhen Library](https://www.szlib.org.cn/)
- [Shenzhen Library OPAC](https://www.szlib.org.cn/opac/)
- [Shenzhen Library OPAC API](https://www.szlib.org.cn/api/opacservice)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local book-list state and may send configured console or email notifications.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
