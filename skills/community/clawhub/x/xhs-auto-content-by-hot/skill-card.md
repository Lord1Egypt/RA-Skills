## Description:

Generates Xiaohongshu content from Baidu hot topics or a custom topic, producing short-form copy plus Seedream-generated cover and supporting images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18923236683](https://clawhub.ai/user/18923236683)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to turn a trending or supplied topic into a Xiaohongshu-ready title, body copy, and image set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to save a user API key directly into generate.py, which can persist a secret in source code.

Mitigation: Use a temporary environment variable or secret store for the API key, and rotate any key that has already been saved in the source file.

Risk: Selected topics and generated prompts are sent to the Volcengine image API.

Mitigation: Avoid using sensitive, private, or confidential topics, and review prompts before sending them to the image service.

Risk: Generated social media copy is based on live or user-provided topics and may be inaccurate, misleading, or unsuitable for publication.

Mitigation: Review and edit the title, body copy, and images before posting them publicly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18923236683/skills/xhs-auto-content-by-hot)
- [Baidu hot topics API endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Volcengine Ark image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Console text plus JSON metadata, text files, and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes selected_topic.txt, xhs_content.json, generated_images.json, and xhs_final_N.png files; image generation requires a Volcengine API key.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
