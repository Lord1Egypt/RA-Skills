## Description: <br>
Creates WeChat Moments and WeChat public-account marketing copy plus structured image prompts and poster assets from a product or service brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, founders, and content teams use this skill to gather campaign details, draft concise Chinese WeChat marketing copy, create image-generation prompts, and assemble a WeChat-ready copy-and-poster package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires credentials for image-generation services and may send prompt content to external providers. <br>
Mitigation: Use dedicated, scoped credentials and avoid entering sensitive business details, private phone numbers, QR codes, or regulated content unless external processing is approved. <br>
Risk: Callback mode can expose a local service and stores callback payloads on disk. <br>
Mitigation: Prefer polling; when callbacks are required, bind only to localhost or a protected interface, add authentication, and clean the callback directory after use. <br>
Risk: Generated files can retain campaign details, contact information, prompt text, and QR-code references. <br>
Mitigation: Review output directories before sharing or archiving and remove private campaign artifacts that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeffli2002/wechat-post-gpt-image2) <br>
- [GPT Image-2 prompt index](gpt-image-2-prompt-index.md) <br>
- [QR code configuration](references/config/qrcode-schema.md) <br>
- [Copy workflow template](references/workflow/copy-template.md) <br>
- [Image layout workflow](references/workflow/image-layout.md) <br>
- [Prompt library referenced by the skill](https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, image prompts, shell command examples, configuration snippets, and generated PNG asset paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write campaign files under wechat-post/{topic-slug}/ and may call external image-generation services when credentials are configured.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
