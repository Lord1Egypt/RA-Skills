## Description:

为微信小店、视频号、社群和朋友圈生成与编辑商品卡、私域海报、直播预告和复购图片，并支持参考图输入与 AI Hive 自动生成下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, store operators, and marketing teams use this skill to create or edit product-card images, private-domain posters, livestream covers, social images, and repeat-purchase visuals for WeChat Shop and related WeChat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key and can read it from the command line, environment, or local config file.

Mitigation: Use a dedicated, revocable API key and avoid exposing local config or shell history.

Risk: Selected product or reference media are uploaded to AI Hive for generation or editing.

Mitigation: Upload only media the user is allowed to share and remove private customer, user, or confidential business information first.

Risk: Custom base URLs can send credentials and media to an endpoint other than the default AI Hive service.

Mitigation: Use the default endpoint unless the alternate endpoint is fully trusted.

Risk: Generated result files are downloaded from remote URLs and saved locally.

Mitigation: Review downloaded outputs before publication and save them to an expected, controlled output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/wechat-shop-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; generated outputs are downloaded image files or JSON task records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials, optional reference images, batch count, model parameters, routing mode, output directory, and no-download mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
