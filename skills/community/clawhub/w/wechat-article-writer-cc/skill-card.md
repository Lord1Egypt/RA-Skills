## Description:

WeChat Article Writer guides users through a multi-phase WeChat Official Account article workflow for requirements clarification, research, outline co-creation, drafting, structured review, header and footer completion, media planning, title and summary optimization, article comparison, and long-article series splitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to plan, draft, review, polish, and package Chinese WeChat Official Account articles. It also supports style-library use, article comparison, and splitting longer drafts into a series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use private writing samples and drafts to infer style.

Mitigation: Keep confidential drafts out of the skill folder unless that use is intended, and review or remove local style summaries after use.

Risk: The skill may persist progress and style details in local files.

Mitigation: Review generated style and creation-log files before sharing the workspace or publishing outputs.

Risk: Research and media-generation steps may rely on external tools even though the artifact includes local-only wording.

Mitigation: Confirm external search, image, or video generation before use, especially when drafts contain private or embargoed material.

Risk: Broad activation phrases and strong workflow language may steer an agent into long, multi-step behavior.

Mitigation: Use the skill for intended WeChat article workflows and keep user instructions explicit when only a narrow review or edit is needed.

## Reference(s):

- [Brief Template](artifact/references/brief-template.md)
- [Research Guide](artifact/references/research-guide.md)
- [Research Templates](artifact/references/research-templates.md)
- [Style Guide](artifact/references/style-guide.md)
- [Review Checklist](artifact/references/review-checklist.md)
- [Header and Footer Templates](artifact/references/header-footer-templates.md)
- [Media Guide](artifact/references/media-guide.md)
- [Article Compare Guide](artifact/references/article-compare.md)
- [Series Split Guide](artifact/references/series-split.md)
- [Creation Log Template](artifact/references/creation-log-template.md)
- [ClawHub Skill Page](https://clawhub.ai/chenchen913/skills/wechat-article-writer-cc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown article drafts, briefs, outlines, review tables, title and summary options, and media resource prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local style summaries and creation logs as part of the article workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
