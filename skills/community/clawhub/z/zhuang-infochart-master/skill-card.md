## Description:

Creates high-quality image-generation prompts for knowledge visuals, article illustrations, concept explainers, flow diagrams, data charts, and infographics, with optional image generation after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text, data, workflows, methods, or concepts into structured prompts for GPT Image 2 style information visuals. After review and approval, the skill can save run artifacts and optionally render images through a configured provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text and reference image URLs may be sent to a configured third-party image provider.

Mitigation: Use the renderer only with approved provider terms and avoid sensitive or proprietary prompts unless that provider policy allows it.

Risk: A live provider API key could be stored in plaintext configuration.

Mitigation: Prefer an environment variable or secret manager and avoid committing populated config.json files.

Risk: Run folders may retain prompts, generation requests, provider result metadata, and image URLs.

Mitigation: Review and clean run folders when tasks contain confidential material or provider-returned URLs.

Risk: Remote image downloads in the optional renderer have limited safeguards.

Mitigation: Use trusted image sources for edit references and inspect downloaded outputs before reuse or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/billzhuang6569/skills/zhuang-infochart-master)
- [Style Catalog](references/style_catalog.md)
- [Data Chart Prompt Templates](references/prompt_result/数据图表)
- [Flow Diagram Prompt Templates](references/prompt_result/流程图)
- [Concept Explanation Prompt Templates](references/prompt_result/概念解释)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown response containing a final English image prompt, Chinese explanation, approval question, and optional run-folder files or generated images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional generation writes request metadata, provider result metadata, prompt files, and image files into a task-specific run folder.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
