## Description:

Generates Chinese social media copy for Xiaohongshu, Douyin, WeChat, and Zhihu from a topic plus optional tone, length, keywords, and audience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bandwe](https://clawhub.ai/user/bandwe)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and operators can use this skill to draft platform-specific Chinese posts, titles, and tags for common social media publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a hardcoded DashScope API key.

Mitigation: Remove the embedded key, rotate the exposed credential, and require users to provide their own provider credentials through explicit configuration.

Risk: Prompt details may be transmitted to Alibaba DashScope when remote generation is activated.

Mitigation: Disclose the remote-provider path clearly and require explicit user opt-in before sending topics, keywords, audience details, or generated prompts to a third-party service.

Risk: The CLI can write generated content to caller-supplied output paths.

Mitigation: Constrain output writes to an expected directory or require review of output paths before running the skill in shared or sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bandwe/skills/social-media-copywriter-generator)
- [DashScope compatible-mode chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted Chinese copy, title lists, tags, CLI status text, and optional output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports platform, tone, length, keywords, audience, titles-only, no-tags, and output-file options.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
