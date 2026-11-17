## Description:

Drafts Xiaohongshu/RED posts, generates cover images, routes drafts for approval, and supports browser-based or manual publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinplezhang](https://clawhub.ai/user/vinplezhang)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, content teams, and agents assisting them use this skill to prepare Xiaohongshu posts, generate platform-sized covers, collect user approval, and publish through a controlled browser session or manual fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in browser session to publish content to Xiaohongshu.

Mitigation: Review every draft, cover image, and hashtag set before approval; keep per-post approval explicit and avoid cron configurations that publish without fresh approval.

Risk: Browser automation, login state, or image upload behavior may fail during publishing.

Mitigation: Verify the browser target and login state before publishing, and use the documented manual copy-paste fallback when automation or uploads fail.

Risk: Generated public social content may be inaccurate, inappropriate, or off-brand.

Mitigation: Have the user review all text, claims, visuals, and tags before any publishing action.

## Reference(s):

- [Content Guide](references/content-guide.md)
- [Browser Publishing Guide](references/browser-publish.md)
- [Xiaohongshu Creator Portal](https://creator.xiaohongshu.com/publish/publish)
- [ClawHub Skill Page](https://clawhub.ai/vinplezhang/skills/vinplezhang-xiaohongshu-publisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown drafts, shell commands, generated PNG cover files, and browser publishing guidance or actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before publishing and supports manual copy-paste fallback when browser automation is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
