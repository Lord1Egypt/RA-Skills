## Description:

Drafts Xiaohongshu/RED posts, generates cover images, routes drafts for user review, and publishes approved posts through browser automation or a manual fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuf1011](https://clawhub.ai/user/yuf1011)

### License/Terms of Use:


## Use Case:

External creators, marketers, and operators use this skill to draft Xiaohongshu content, generate a 1080x1440 PNG cover, review the proposed post, and publish it after explicit approval. It can also package the content for manual posting when browser automation is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated covers include OpenClaw branding by default, which may be unclear to users or unsuitable for a given post.

Mitigation: Review the generated cover before publishing and override the badge text when the brand label should be changed or removed.

Risk: Scheduled posting guidance could affect a live Xiaohongshu account without timely human oversight.

Mitigation: Keep scheduled runs draft-only and require explicit user approval before any browser-based publish action.

Risk: The skill needs access to a logged-in Xiaohongshu creator session and browser automation may fail or encounter an expired login.

Mitigation: Use only an account the agent is authorized to access, verify login state before publishing, and fall back to manual posting when automation is unavailable.

Risk: The cover-generation script depends on Pillow and local CJK fonts.

Mitigation: Run it in an isolated Python environment with Pillow installed and verify required CJK fonts before relying on generated assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuf1011/skills/xiaohongshu-publisher)
- [Publisher profile](https://clawhub.ai/user/yuf1011)
- [Xiaohongshu creator publishing portal](https://creator.xiaohongshu.com/publish/publish)
- [Browser Publishing Guide](references/browser-publish.md)
- [Xiaohongshu Content Guide](references/content-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown draft text with shell commands, browser automation guidance, and PNG cover image file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a 1080x1440 PNG cover image and may produce manual copy-paste publishing instructions when automation is unavailable.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
