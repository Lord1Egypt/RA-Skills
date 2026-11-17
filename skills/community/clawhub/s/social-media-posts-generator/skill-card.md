## Description:

Generates multi-page social media image carousels from prompt, image, template, style, and asset-size inputs through the Craftsman Agent image generator API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to configure and call an external image-generation service that creates editable social media carousel assets for platforms such as Instagram, X/Twitter, and Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI example uses an unpinned npm package while handling an API key.

Mitigation: Prefer the direct curl/API example; if using the CLI, verify the npm package provenance and version before execution.

Risk: Prompts and images are sent to an external service without enough data-handling disclosure.

Mitigation: Avoid confidential prompts and sensitive images unless the provider's data policy is acceptable.

Risk: The workflow requires an API key for the OneKey Gateway.

Mitigation: Use a narrowly scoped, revocable API key and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/social-media-posts-generator)
- [Craftsman Image Generator Console](https://craftsman-agent.aiagenta2z.com/app/image-generator)
- [Craftsman Website](https://craftsman-agent.aiagenta2z.com)
- [OneKey access keys](https://deepnlp.org/workspace/keys)
- [OneKey Router API endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown instructions with bash commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe API calls that can return image URLs, share URLs, session metadata, and editable carousel layout data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
