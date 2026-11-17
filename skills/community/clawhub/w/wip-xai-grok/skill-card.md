## Description:

xAI Grok API. Search the web, search X, generate images, generate video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to query current web and X information through xAI Grok, then generate or edit images and create short videos from prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, search queries, and media may be sent to xAI services.

Mitigation: Install and use only when that data sharing is acceptable for the intended workload.

Risk: Image editing can read local file paths supplied to the tool.

Mitigation: Avoid local file path inputs for image editing unless the skill is updated to restrict paths and file sizes.

Risk: If XAI_API_KEY is not set, the skill may try to read an xAI API key from 1Password.

Mitigation: Set an explicit XAI_API_KEY for controlled deployments and review local 1Password access before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-xai-grok)
- [Project homepage](https://github.com/wipcomputer/wip-xai-grok)
- [xAI API base](https://api.x.ai/v1)
- [xAI Web Search documentation](https://docs.x.ai/developers/tools/web-search)
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Image Generation documentation](https://docs.x.ai/docs/guides/image-generations)
- [xAI Video Generation documentation](https://docs.x.ai/docs/guides/video-generations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown, JSON, shell commands, configuration snippets, and generated media URLs or base64 data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search outputs may include citations and usage metadata; generated image and video URLs are temporary.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
