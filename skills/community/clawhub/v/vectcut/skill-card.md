## Description:

VectCut orchestrates cloud video-editing workflows for talking-head cuts, remix videos, ecommerce ads, subtitles, audio, effects, picture-in-picture, AI-generated media, draft download, and Feishu Bitable automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sun-guannan](https://clawhub.ai/user/sun-guannan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video operations teams use this skill to assemble automated VectCut editing workflows that create or modify drafts, upload local media, add subtitles, audio, effects, templates, AI-generated media, and export rendered videos. It can also turn an existing video-production process into Feishu Bitable fields and workflow prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key exposure could occur if the skill prints, pastes, or embeds VECTCUT_API_KEY in generated prompts or chat output.

Mitigation: Use protected secret references or environment injection only; do not echo, print, paste, or store the raw key in workflow prompts.

Risk: The skill can use VectCut account access to create drafts, upload media, process assets, and render videos.

Mitigation: Install only in trusted workspaces, use the least-privileged VectCut account available, and review draft, upload, and render actions before running workflows.

Risk: Generated Feishu Bitable workflow prompts may carry sensitive workflow or credential material if not reviewed.

Mitigation: Review generated Feishu prompts before use and replace any credential material with protected secret references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sun-guannan/skills/vectcut)
- [VectCut homepage](https://www.vectcut.com/)
- [VectCut API documentation index](https://docs.vectcut.com/llms.txt)
- [Model capabilities reference](artifact/references/model_capabilities.json)
- [AI image model capabilities reference](artifact/references/ai-image-model_capabilities.json)
- [Cover prompt references](artifact/references/cover_prompt_references.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands; bundled scripts may emit JSON result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VECTCUT_API_KEY; outputs may include draft IDs, draft URLs, rendered video URLs, uploaded media URLs, workflow summaries, or Feishu Bitable workflow prompts.]

## Skill Version(s):

1.5.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
