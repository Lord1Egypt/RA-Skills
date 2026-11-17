## Description:

Extract and summarize publicly accessible WeChat Work pages, including announcements, app information, and group invitations, without internal API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing public WeChat Work share pages use this skill to extract titles, authors, update times, summaries, app details, version information, links, and invitation-page notes without accessing private enterprise data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be misapplied to private chats, tenant data, admin actions, authenticated workflows, or pages requiring internal permissions.

Mitigation: Use it only for public WeChat Work share, announcement, app, or invitation pages, and do not provide credentials or private enterprise links.

Risk: Dynamic public pages may be incomplete if summarized before client-side content finishes rendering.

Mitigation: Wait for page rendering before extracting fields, then verify key details such as title, author, update time, and source link.

Risk: Repeated access to public pages can create unnecessary traffic or conflict with platform expectations.

Mitigation: Apply frequency controls and avoid repeated visits when the same public content has already been collected.

## Reference(s):

- [WeChat Work](https://work.weixin.qq.com/)
- [ClawHub Skill Page](https://clawhub.ai/mike47512/skills/wechat-work)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or concise text summaries with extracted field lists and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are limited to publicly accessible page content and do not include private tenant, chat, admin, or authenticated workflow data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
