## Description:

Use when generating a complete WeChat article from a topic, with optional source research, evidence tracking, illustration, HTML conversion, and draft-box publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhylq](https://clawhub.ai/user/zhylq)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and developers use this skill to create WeChat public-account articles from a topic or reference URLs, including source collection, drafting, review, polishing, and optional publishing preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated drafts, images, and metadata may be sent to external providers and WeChat by default.

Mitigation: Set post_to_wechat to false unless a remote WeChat draft is intended, and disable optional illustration or upload steps when external transfer is not acceptable.

Risk: Optional publishing and illustration steps depend on auxiliary skills and credentials.

Mitigation: Review and scope the auxiliary skill credentials before use, especially WeChat and image-provider settings.

Risk: Unpinned installation can change behavior across releases.

Mitigation: Prefer installing from a pinned commit or reviewed release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhylq/skills/zhy-wechat-writing)
- [ClawHub publisher profile](https://clawhub.ai/user/zhylq)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Files, Guidance]

**Output Format:** [Markdown article files, evidence and review notes, optional illustrated Markdown, optional WeChat-styled HTML, and an execution summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are typically written under articles/<slug>/ and may include article.md, sources/evidence.md, sources/review.md, article.illustrated.md, illustrations, article.zhy.html, word count, review score, and WeChat draft status.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; source skill frontmatter declares 3.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
