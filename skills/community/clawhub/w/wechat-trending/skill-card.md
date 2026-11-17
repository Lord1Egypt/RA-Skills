## Description:

Extracts and summarizes publicly accessible WeChat shared pages, including announcements, app information, and group invitation details, without login or private data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to extract titles, authors, update times, summaries, tags, and source links from publicly accessible WeChat announcements, app pages, and group invitation pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misapplied to private chats, restricted group content, account login, messaging, or permission bypass.

Mitigation: Use it only with public WeChat URLs or explicit public-page extraction tasks, and do not provide account credentials or private content.

Risk: Repeated extraction from public pages could create unnecessary traffic or stale summaries if dynamic content has not finished loading.

Mitigation: Apply frequency controls, wait for public page rendering to complete, and include the source link with generated summaries.

## Reference(s):

- [WeChat Official Site](https://weixin.qq.com/)
- [ClawHub Skill Release](https://clawhub.ai/codekungfu/skills/wechat-trending)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should be limited to public page content and should include source links when available.]

## Skill Version(s):

0.1.0 (source: release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
