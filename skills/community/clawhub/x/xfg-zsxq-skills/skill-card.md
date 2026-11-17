## Description:

Automates ZSXQ knowledge community workflows including posting, replies, browsing posts, notification checks, article drafts, and scheduled checks using saved account session configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzhengwei](https://clawhub.ai/user/fuzhengwei)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent manage ZSXQ community posting, replies, article drafts, notification review, and recurring checks from local session configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full ZSXQ session cookies or tokens that can read account data and publish as the user.

Mitigation: Use a dedicated account or least-privileged session where possible, keep cookies out of shell history and shared files, and rotate any token that may have been exposed.

Risk: Saved credentials can be used to post, reply, or publish article drafts without re-entering the cookie.

Mitigation: Review the configured target group before each publishing action and remove saved credentials when automation is no longer needed.

Risk: Recurring checks create persistent access patterns that may continue after initial setup.

Mitigation: Enable scheduled jobs only when recurring access is intended, review the generated schedule, and disable or remove the job when it is no longer required.

Risk: Documentation includes a real-looking token example that could encourage unsafe credential copying.

Mitigation: Replace example tokens with placeholders before distribution and rotate any credential copied into logs, documentation, or command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzhengwei/skills/xfg-zsxq-skills)
- [Publisher profile](https://clawhub.ai/user/fuzhengwei)
- [ZSXQ web app](https://wx.zsxq.com)
- [Puppeteer documentation](https://pptr.dev)
- [API reference](references/api.md)
- [Usage guide](references/usage.md)
- [Signature reference](references/signature.md)
- [Token configuration](references/token-config.md)
- [Browser automation reference](references/puppeteer.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated API request behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local ZSXQ configuration files and scheduled-job configuration when the user runs the provided scripts.]

## Skill Version(s):

2.3.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
