## Description:

通过 OpenClaw 浏览器在抖音创作者平台准备图文文章草稿，填写标题、摘要、正文、头图、话题和配乐，并将最终发布留给用户确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to have an agent prepare a Douyin Creator article draft with article text, cover art, topics, and music. The skill saves the draft and leaves publication to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent operates a Douyin Creator browser session and may prepare content, cover, topic, and music selections that affect a public-facing post.

Mitigation: Review the generated draft, cover, topics, and music in Douyin Creator before manually publishing.

Risk: The workflow depends on live Douyin Creator page structure and may select the wrong control if the interface changes.

Mitigation: Have the agent take fresh page snapshots during each step and confirm the saved draft before publication.

## Reference(s):

- [Douyin Creator article upload page](https://creator.douyin.com/creator-micro/content/upload?default-tab=5)
- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/publish-douyin-article-infinite)

## Skill Output:

**Output Type(s):** [Text, Guidance, Browser commands]

**Output Format:** [Markdown-style procedural guidance for browser-driven draft preparation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a saved Douyin article draft; final publishing remains manual.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
