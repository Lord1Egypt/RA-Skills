## Description:

Extract and summarize publicly shared WeChat pages, including announcements, app details, and group invitations, without login or account access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract key details and summaries from public WeChat share pages, public app or announcement pages, and public group invitation pages. It is not intended for login-protected content, messaging, credential use, or private account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be misapplied to private, login-protected, or account-specific WeChat content.

Mitigation: Use it only with publicly accessible share links and do not provide WeChat credentials or request messaging or account actions.

Risk: Summaries of dynamically loaded public pages may omit or misstate details if content is parsed before rendering completes.

Mitigation: Wait for page rendering to complete and review extracted titles, authors, update times, summaries, tags, and links before relying on them.

## Reference(s):

- [WeChat homepage](https://weixin.qq.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/wechat-hot-trend)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs titles, authors, update times, summaries, tags, version details, links, and usage notes for public pages only.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
