## Description:

为天猫旗舰店生成与编辑商品页视频、品牌故事、新品首发、详情演示、大促会场和会员内容，支持 Seedance 多模式及 AI Hive 自动交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand teams, and developers use this skill to generate and adapt Tmall flagship-store videos for product pages, brand hero placements, product launches, promotional campaign bases, and member-retention content. It helps structure prompts and shell commands for Seedance video generation, reference-based generation, editing, and extension through AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI Hive API credentials.

Mitigation: Use only trusted AI Hive endpoints, prefer environment-based secrets where possible, keep the generated config file private, and rotate keys if they may have been exposed.

Risk: The skill can write downloaded generation results to disk.

Mitigation: Run it in an isolated workspace, review output directories before use, and avoid processing untrusted result URLs or filenames until publisher-side validation is strengthened.

Risk: Custom API base URLs can redirect requests to an unintended service.

Mitigation: Avoid custom base URLs unless the operator controls and trusts the endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/tmall-ecommerce-video-generation-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates prompts and command patterns for video generation, upload, task polling, and downloaded media outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
