## Description:

Automates conversion of Markdown articles into WeChat Official Account-ready HTML and creates draft posts with optional cover generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanbinsite](https://clawhub.ai/user/hanbinsite)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to prepare Markdown article directories, generate or supply cover images, and create WeChat Official Account drafts for review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat account credentials and optional AI image API keys.

Mitigation: Use trusted credentials only, keep secrets out of committed .env files and examples, and rotate credentials if they are exposed.

Risk: The AI image configuration can send a bearer token and prompts to a configurable endpoint.

Mitigation: Set AI_IMAGE_BASE_URL only to trusted HTTPS providers and prefer the base64 image generation path over URL downloads.

Risk: Article content, cover prompts, images, and publishing metadata may be sent to external WeChat or AI services.

Mitigation: Review content before publishing and confirm that external service use is acceptable for the article material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanbinsite/skills/wechat-publish-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat draft IDs and local cover image files when the supplied scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
