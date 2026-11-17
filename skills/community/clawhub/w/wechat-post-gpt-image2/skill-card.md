## Description:

微信公众号/朋友圈营销内容智能体。输入产品/服务主题、卖点、讲师信息、配图需求，输出专业文案+结构化配图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, creators, and developers use this skill to generate WeChat Moments or official-account marketing copy, image prompts, and poster assets from product, selling-point, pricing, instructor, and QR-code inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The callback server may be exposed publicly without authentication.

Mitigation: Prefer polling-only operation, or bind callbacks to localhost or a protected host with authentication and firewall controls.

Risk: Generated prompts, product details, contact information, QR assets, and image URLs may be sent to third-party image services.

Mitigation: Review input data before submission, avoid sensitive personal or business information, and use a limited API key.

Risk: Downloaded image URLs and generated files may write into local output directories.

Mitigation: Use a dedicated output directory and review downloaded assets before publishing or redistributing them.

## Reference(s):

- [GPT Image-2 Prompt Matching Index](gpt-image-2-prompt-index.md)
- [QR Code Configuration](references/config/qrcode-schema.md)
- [Copy Template](references/workflow/copy-template.md)
- [Image Layout - WeChat Moments Poster](references/workflow/image-layout.md)
- [Prompt case library](https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with generated copy, image prompts, file paths, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local output files under wechat-post/{topic-slug}/, including copy.md, image-prompt.md, qrcode_setting.txt, PNG poster assets, and a combined delivery Markdown file.]

## Skill Version(s):

2.1.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
