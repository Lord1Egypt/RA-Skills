## Description:

Seedream 5.0 Lite 图片编辑 helps agents edit authorized images through dependency-ordered prompts for object removal, color replacement, outpainting, background cleanup, lighting changes, and AI Hive task handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare structured image-edit instructions, run fixed-model Seedream 5.0 Lite edits through AI Hive, and check that protected facts, geometry, identities, logos, and text remain unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs an AI Hive API key and can persist that key in local configuration.

Mitigation: Use a dedicated API key, keep local configuration private, prefer a dedicated Python environment, and avoid running the helper with elevated privileges.

Risk: The helper uploads the exact images passed on the command line and downloads results from service-provided URLs.

Mitigation: Use only images authorized for upload, avoid sensitive images or restricted-network contexts, and review URL handling before higher-risk use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-image-edit)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and Python helper calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload command-line image inputs, submit AI Hive image-edit tasks, poll task status, and download generated image files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
