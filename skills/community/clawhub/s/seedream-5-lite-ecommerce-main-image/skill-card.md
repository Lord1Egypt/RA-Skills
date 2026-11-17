## Description:

使用 Seedream 5.0 Lite 通过商品事实、渠道规范、缩略图识别和促销合规四道闸门制作电商主图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, listing operators, and agent users use this skill to generate Seedream 5.0 Lite product main-image candidates for marketplace listings. The workflow emphasizes SKU accuracy, channel presentation rules, thumbnail legibility, and review of promotional or efficacy claims before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images, reference images, prompts, and API keys are handled through AI Hive and local configuration.

Mitigation: Install only if that data handling is acceptable, use a dedicated API key, and keep local key files restricted.

Risk: The skill can overstate ecommerce compliance because platform rules, SKU facts, and promotional claims still require human judgment.

Mitigation: Manually verify SKU accuracy, current platform rules, channel-specific presentation constraints, and any promotional or efficacy claims before publishing.

Risk: Network download handling and output paths deserve review before routine use.

Mitigation: Use an isolated Python environment and a dedicated output directory until URL allowlisting, filename sanitization, download limits, data-handling disclosure, and pinned dependencies are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-ecommerce-main-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and generated image files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY or a local AI Hive config file; generated image results are saved to a user-selected or default output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
