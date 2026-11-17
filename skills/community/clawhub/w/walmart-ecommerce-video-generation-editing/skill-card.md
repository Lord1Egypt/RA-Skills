## Description:

Create and edit Walmart Marketplace product videos, assembly guides, package-content demonstrations, variant clips, and retail advertising bases for Walmart商品视频、Marketplace listing video、零售产品演示、安装教程、包装清单、SKU套装、家庭场景, and 广告素材 with Seedance generation/editing through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace sellers, retail creative teams, and developers use this skill to generate and edit item-page product videos, assembly guides, package-content demonstrations, variant clips, and retail ad bases that stay aligned with the item record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key and stores or reads credentials from the user's environment or ~/.ai-hive/config.json.

Mitigation: Use a dedicated API key with limited exposure, inspect ~/.ai-hive/config.json before use, keep the file private, and rotate the key if it is shared or exposed.

Risk: The skill sends selected product media and prompts to AI Hive/Seedance services for generation and editing.

Mitigation: Upload only media approved for the item workflow and avoid confidential, personal, or unapproved product assets.

Risk: The base URL can be customized, which may redirect credentials and media to an unintended endpoint.

Mitigation: Use the default AI Hive endpoint or a fully controlled endpoint, and review any custom base URL before running generation commands.

Risk: Generated retail videos can misstate product facts, quantities, prices, claims, availability, or platform requirements.

Mitigation: Lock the item truth record before generation and review outputs against the catalog record, safety instructions, package contents, and current Walmart Marketplace requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/walmart-ecommerce-video-generation-editing)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API Base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API Key Console](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands, configuration examples, and AI Hive video-generation task references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and may upload selected product media to AI Hive/Seedance services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
