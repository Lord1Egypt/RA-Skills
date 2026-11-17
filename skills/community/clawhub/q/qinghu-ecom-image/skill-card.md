## Description:

一键生成电商商品图：商品主图+轮播图套图、电商详情页长图、按文字描述直出商业大图（四个自定义生图模型，支持参考图）。适用于抖音、淘宝天猫、拼多多、京东、1688、Amazon、TikTok、Shopee、Ozon 等平台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and commerce content creators use this skill to route product-image requests to Qinghu AI for listing images, carousel sets, detail-page graphics, and custom promotional visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded product images may contain material unsuitable for processing or subject to service retention terms, and image generation uses credits.

Mitigation: Upload only images suitable for Qinghu processing and review its retention terms and credit costs.

Risk: An API key could be exposed if mishandled, and the separately downloaded qhkit CLI was not audited as part of the supplied artifact review.

Mitigation: Keep the API key private; prefer a reviewed, pinned CLI version and run it with limited permissions.

## Reference(s):

- [@iqinghu/qhkit on npm](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance, JSON command parameters, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the qhkit CLI; image count and output type vary by selected generation mode.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
