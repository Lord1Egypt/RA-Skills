## Description:

Builds platform-specific publish packages and verifies long-form images, real card files, manifests, human gates, public URLs, and release readiness for reviewed content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Content publishers and agents use this skill to generate preflight publish packages for WeChat, Zhihu, Zhihu Idea, Xiaohongshu, blog, or multi-platform drafts, then verify real images, manifests, URLs, human gates, and blockers before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated publish packages may contain public URLs, image paths, account details, tag freshness claims, or release status that require editorial review.

Mitigation: Review every generated package before use, especially URL accessibility, image paths, account details, tag freshness evidence, and remaining blockers.

Risk: A package could appear publish-ready even when real card images, manifests, visual QA, or human confirmation are incomplete.

Mitigation: Keep packages at needs_review or blocked until real files, manifest paths, image order, dimensions, visual QA, and human confirmation are explicitly recorded.

Risk: Current or trending tags can become misleading when freshness has not been checked during the run.

Mitigation: Mark hot tags unverified unless current values, source, and checked_at timestamp are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/wenchang-publish-check)
- [Source homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-publish-check)
- [Publisher profile](https://clawhub.ai/user/yangchao228)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown publish package with structured status, blocker, platform, image, and handoff sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update content_state with file pointers, statuses, blockers, and next handoff; does not upload files, generate images, or publish externally.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
