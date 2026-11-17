## Description:

生成与编辑小红书笔记首图、种草封面、好物清单封面和品牌合作视觉，支持人物与商品参考图、中文标题留白、批量创意方向及 AI Hive 自动下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content operators use this skill through an agent to prepare Xiaohongshu/RED cover-image workflows, generate or edit cover images from reference assets, and retrieve AI Hive image-generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key.

Mitigation: Store the key only through the intended environment variable or local config file, keep local config permissions restricted, and rotate the key if it is exposed.

Risk: Selected reference images are uploaded to AI Hive for generation or editing.

Mitigation: Review file paths before execution and avoid private or sensitive images unless uploading them to AI Hive is intended.

Risk: Generated covers could imply unsupported claims, product results, prices, endorsements, or commercial disclosures.

Mitigation: Review titles, brand text, claims, pricing, experience conclusions, and sponsorship disclosures before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/xiaohongshu-viral-cover-image-generation)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Image files, JSON]

**Output Format:** [Markdown guidance with bash command examples; generated image tasks download PNG files or return JSON when downloads are disabled.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; may upload selected reference images to AI Hive and saves downloaded results to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
