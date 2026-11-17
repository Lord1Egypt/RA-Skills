## Description:

AI Xiaohongshu Post Generator generates editable, Xiaohongshu-ready posts and slides with AI-created content, captions, images, text blocks, storylines, and backgrounds for formats such as knowledge cards, posters, and movie introductions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to generate social-media card sets and editable post assets for Xiaohongshu and related channels from prompts and optional reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npx onekey command path.

Mitigation: Pin or otherwise verify the CLI package before use, and run it in a restricted environment.

Risk: The skill requires a DeepNLP/OneKey access key for external API calls.

Mitigation: Use a least-privilege key and avoid exposing it in logs, shared terminals, or generated artifacts.

Risk: Prompts and reference images may be uploaded to external services.

Mitigation: Avoid submitting confidential prompts, proprietary images, or sensitive campaign materials unless the service's data handling is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/xiaohongshu-post-generator)
- [Craftsman Social Media Posts Generator](https://craftsman-agent.aiagenta2z.com/app/social-media-posts)
- [DeepNLP Workspace Keys](https://deepnlp.org/workspace/keys)
- [OneKey Router Endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and npx command examples plus JSON request and response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The backing service can return share URLs, generated image URLs, editable page-layer data, and export-ready social post assets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
