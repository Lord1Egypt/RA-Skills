## Description:

Create and publish Xiaohongshu (RED) notes through API posting, browser automation, or draft generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antaeus001](https://clawhub.ai/user/antaeus001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and publish Xiaohongshu notes, including title, body, and hashtag drafting, API posting for approved accounts, browser-assisted posting for personal accounts, and draft-only output for manual publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser mode can expose authenticated Xiaohongshu page contents and account actions to a model-driven workflow.

Mitigation: Prefer draft-only or API mode where possible; use browser mode only with a local or self-hosted analyzer endpoint and a dedicated browser profile.

Risk: Automated browser publishing can act inside a logged-in personal account and may submit unintended content.

Mitigation: Review the note content and publishing page before final submission, and keep sensitive accounts or clipboard data out of the browser session.

Risk: Debug and step modes can save screenshots or page HTML that may contain sensitive account information.

Mitigation: Avoid debug capture for normal use; if debugging is necessary, inspect and remove saved artifacts after troubleshooting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antaeus001/skills/xiaohongshu-post-antaeus)
- [API Setup Guide](references/api-setup.md)
- [Xiaohongshu Open Platform](https://open.xiaohongshu.com)
- [Xiaohongshu Open Platform Documentation](https://school.xiaohongshu.com/open)
- [Xiaohongshu Creator Console](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts can emit draft text or JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API posting results, browser automation status messages, and formatted draft content for manual publishing.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
