## Description:

Deprecated HeyGen skill that helps an agent generate and manage AI avatar videos with legacy v1/v2 endpoints while directing users to current v3 replacement skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelwang11394](https://clawhub.ai/user/michaelwang11394)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to guide HeyGen avatar video generation, prompt optimization, video status polling, asset upload, captions, templates, and webhook workflows. Because this release is deprecated, users should prefer the current create-video or avatar-video skills for new v3 API work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad HeyGen account-changing actions using HEYGEN_API_KEY.

Mitigation: Use only an API key you are comfortable letting an agent use, and review the skill before installation.

Risk: Delete actions may remove videos or related resources.

Mitigation: Require explicit manual confirmation before any delete action is executed.

Risk: Upload workflows may send sensitive media to HeyGen.

Mitigation: Avoid uploading sensitive media and validate file type, size, and content before upload.

Risk: URL-based ingestion can fetch arbitrary remote content.

Mitigation: Use strict allowlists and size limits before allowing an agent to ingest URLs.

Risk: Public webhook endpoints can expose event data or accept untrusted requests.

Mitigation: Secure webhook endpoints before public exposure and verify event origin or signatures.

## Reference(s):

- [HeyGen Video Agent API documentation](https://docs.heygen.com/reference/generate-video-agent)
- [Skill definition](SKILL.md)
- [HeyGen Authentication](references/authentication.md)
- [Video Agent API](references/video-agent.md)
- [Video Generation](references/video-generation.md)
- [Video Status and Polling](references/video-status.md)
- [Asset Upload and Management](references/assets.md)
- [HeyGen Quota and Credits](references/quota.md)
- [HeyGen Avatars](references/avatars.md)
- [HeyGen Voices](references/voices.md)
- [Video Agent Prompt Optimizer](references/prompt-optimizer.md)
- [Visual Style Library](references/visual-styles.md)
- [Webhooks](references/webhooks.md)
- [HeyGen and Remotion Integration](references/remotion-integration.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with API examples, command snippets, and structured request configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP tool calls or direct HeyGen API requests that require HEYGEN_API_KEY.]

## Skill Version(s):

2.23.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
