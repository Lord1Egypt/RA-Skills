## Description:

Routes content requests or content_state records to the next Wenchang workflow stage for WeChat, Zhihu, Zhihu Idea, Xiaohongshu, blog, or multi-platform delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Content workflow operators, creators, and agent users use this skill to identify the current Wenchang stage, active platform branch, blockers, and the next skill or stop condition before drafting, image handling, URL planning, or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend downstream skills that perform research, image handling, URL upload planning, or publishing checks.

Mitigation: Treat its recommendation as routing guidance and require explicit user confirmation before uploads, paid generation, or publication.

Risk: Incomplete evidence, review status, visual QA, or human confirmation can make a content package unready for release.

Mitigation: Use the returned blockers and content_state update to route back to research, review, image QA, or a human gate before final publish checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/wenchang-router)
- [Project homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/content/wenchang-router)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown routing decision with a YAML content_state update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files are generated; high-impact external actions are gated for user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
