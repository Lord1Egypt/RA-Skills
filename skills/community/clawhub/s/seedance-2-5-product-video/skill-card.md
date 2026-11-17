## Description:

用 Seedance 2.5 把真实商品图和产品主档变成可剪辑的产品宣传片镜头包，覆盖 Hero、材质微距、机构演示、人与产品互动、尺度证明和品牌结尾。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and commerce operators use this skill to create product-video shot plans and AI Hive generation commands for launch films, marketplace videos, social commerce clips, and product-detail pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images or reference videos are uploaded to AI Hive when generation runs.

Mitigation: Use --preview before submitting, avoid sensitive or unapproved assets, and proceed only when AI Hive processing is acceptable.

Risk: The auth command can store an AI Hive API key in ~/.ai-hive/config.json.

Mitigation: Prefer AI_HIVE_API_KEY for temporary use, or remove ~/.ai-hive/config.json when the saved credential is no longer needed.

Risk: Generated footage can misrepresent product facts, sizes, mechanisms, or claims.

Mitigation: Use approved product sources and fact sources for mechanism, interaction, and scale shots, then review each shot before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-5-product-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands, JSON preview output, task status text, and optional downloaded MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-specified product images and optional motion reference videos; preview mode emits the request without upload or billing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
