## Description: <br>
Content Engine deconstructs Xiaohongshu posts into structured analysis and generates brand-adapted scripts, captions, covers, descriptions, tags, image references, and optional Seedance video outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, marketers, and agent users use this skill to study Xiaohongshu posts, extract reusable content patterns, and generate brand-specific social content assets from a reference post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses TikHub, Ofox or OpenRouter, and optionally Volcengine Ark credentials, and may send links, brand context, product descriptions, prompts, and generated outputs to those services. <br>
Mitigation: Use dedicated API credentials, avoid running from workspaces with unrelated .env secrets, and review what data will be sent before execution. <br>
Risk: Real video generation can incur Ark API charges. <br>
Mitigation: Use --no-real-video for prompt-only video workflows, keep the built-in cost confirmation enabled, and verify ARK_API_KEY configuration before starting a paid run. <br>
Risk: Generated social content may contain inaccurate, off-brand, or unsuitable claims. <br>
Mitigation: Review generated scripts, captions, descriptions, tags, images, and videos before publishing or sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/qianxun-content-engine-en) <br>
- [Output template](references/output-template.md) <br>
- [Video deconstruction example](references/example-video.md) <br>
- [Image deconstruction example](references/example-image.md) <br>
- [TikHub](https://tikhub.io) <br>
- [Ofox](https://ofox.ai) <br>
- [Volcengine Ark API keys](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Ronin content engine architecture inspiration](https://x.com/DeRonin_/status/2042604279077237170) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown deconstruction cards plus text asset files, prompt files, generated image or video files, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local workspaces and graph updates; real video generation can call Ark and incur API charges unless disabled.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
