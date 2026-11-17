## Description:

Automatically prepares and publishes Xiaohongshu image-text notes by generating post copy, creating square cover images, and driving the creator-center publishing flow with Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harveyzzzz](https://clawhub.ai/user/harveyzzzz)

### License/Terms of Use:


## Use Case:

Content creators and operators use this skill to generate Xiaohongshu note copy, create square cover images, and publish image-text posts through the Xiaohongshu creator center.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to a live Xiaohongshu account without a final confirmation.

Mitigation: Review generated title, body text, and images before running the publish command, and run the skill only when you intend to post.

Risk: Authenticated browser profiles, screenshots, generated content, and HTML debug dumps may remain on disk.

Mitigation: Keep the browser profile and skill data directories private, prefer temporary profiles unless persistence is needed, and periodically delete local skill data.

## Reference(s):

- [Selector Reference](references/selectors.md)
- [ClawHub Skill Page](https://clawhub.ai/harveyzzzz/skills/xhsredbook)
- [Xiaohongshu Creator Center Publish Page](https://creator.xiaohongshu.com/publish/publish)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated post text and PNG cover image files at runtime]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional topic, title, content, cover text, image paths, image count, and browser profile directory.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
