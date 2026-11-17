## Description:

Extract and summarize public QQ app pages, announcements, and group invites without login or message access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract titles, authors, update times, summaries, metadata, version details, and relevant links from publicly accessible QQ pages. It is intended for public announcements, app pages, and group invite pages, not account login, messaging, private content, or permission bypass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misapplied to account actions, private messages, authenticated QQ content, or workflows that require login or permission bypass.

Mitigation: Use it only for publicly accessible QQ pages and review requests before execution to confirm that the target content is public.

Risk: Dynamic QQ pages may render content after initial page load, which can lead to incomplete extraction or summaries.

Mitigation: Wait for page rendering to complete, verify key fields such as title, author, update time, and source link, and keep retries rate-limited.

## Reference(s):

- [QQ Homepage](https://im.qq.com/)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/qq-hot-trend)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are limited to summaries and extracted fields from publicly accessible QQ pages.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
