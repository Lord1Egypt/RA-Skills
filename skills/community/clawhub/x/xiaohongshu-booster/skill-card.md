## Description:

Generate 3 viral-ready Xiaohongshu (Little Red Book) notes from a product, scene, or topic, including titles, body copy, hashtags, cover-image tips, and publish-time recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, social media managers, and agents use this skill to draft localized Xiaohongshu note variants from a topic, product, venue, or scene for review before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated marketing copy can overstate claims, especially for skincare, supplements, or medical-adjacent products.

Mitigation: Review generated claims before posting and include the available disclaimer for sensitive categories.

Risk: The CLI --output option writes to the path supplied by the user.

Mitigation: Use --output only with a path that is acceptable to create or overwrite.

## Reference(s):

- [Xiaohongshu Writing Templates](references/templates.md)
- [Xiaohongshu Hashtag Library](references/hashtags.md)
- [Xiaohongshu Cover Image Tips](references/cover-tips.md)
- [Xiaohongshu Booster on ClawHub](https://clawhub.ai/harrylabsj/skills/xiaohongshu-booster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON containing Xiaohongshu note drafts, metadata, hashtags, cover tips, and publish-time suggestions; documentation also provides Markdown guidance and CLI examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 1 to 5 note variants; the normal documented workflow generates 3 variants and can write JSON to stdout or a user-selected output file.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
