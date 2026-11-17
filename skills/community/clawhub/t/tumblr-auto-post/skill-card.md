## Description:

Generates Fu Sheng-style Chinese articles and optional cover images, gathers topic, audience, writing goal, length, and content preferences, then publishes directly to Tumblr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx-00](https://clawhub.ai/user/lgx-00)

### License/Terms of Use:

MIT-0

## Use Case:

External creators or social media operators use this skill to draft Chinese Tumblr posts, optionally create a cover image, and publish the result to Tumblr. It is intended for users who control the target Tumblr account and can review content before public release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately publish public posts to a fixed Tumblr account using hard-coded OAuth credentials.

Mitigation: Revoke and remove packaged credentials, require user-provided secrets or OAuth, and default to draft or preview before publishing.

Risk: Generated content may be posted without a meaningful preview or approval boundary.

Mitigation: Add a final review step that shows the article, image status, target blog, and publish action before making API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgx-00/skills/tumblr-auto-post)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance]

**Output Format:** [Conversational prompts, HTML-formatted article content, optional image file, and a Tumblr post URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make authenticated Tumblr API calls and publish public posts; cover image generation depends on uv and GEMINI_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
