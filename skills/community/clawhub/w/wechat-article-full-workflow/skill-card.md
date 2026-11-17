## Description:

Guides the full WeChat Official Account article workflow, from topic and title through writing, layout, images, quality checks, draft submission, and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code only); all rights reserved (documentation and theoretical text)

## Use Case:

Content creators and WeChat Official Account editors use this skill to draft, format, check, and submit articles to a draft box for review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled draft-submission script can delete existing WeChat drafts without clear user-controlled confirmation.

Mitigation: Do not run the script with production credentials unless draft deletion is removed or guarded by explicit confirmation.

Risk: The included credential guide and AppID expose sensitive operational details.

Mitigation: Keep account secrets in a proper secret store rather than copying them through shell commands; review the guide before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/wechat-article-full-workflow)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)
- [WeChat article HTML template](references/html-template.md)
- [Writing and title patterns](references/crayon/title-patterns.md)
- [Credential setup guide](references/credentials-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Guidance]

**Output Format:** [Article drafts and WeChat-compatible HTML, with review notes and draft-preview guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submission is to the draft box, not an automatic broadcast.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
