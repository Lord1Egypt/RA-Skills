## Description: <br>
为知识型配图、文章配图、概念解释图、流程图、数据图表和信息图创作高质量生图 Prompt，并可在用户确认后生成图片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billzhuang6569](https://clawhub.ai/user/billzhuang6569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn text, data, workflows, methods, or concepts into polished image-generation prompts for knowledge visuals, charts, flow diagrams, concept explainers, and infographics. With user approval, it can also create a local run folder and generate images through a built-in image tool or configured fal.ai-compatible fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved prompts and optional reference image URLs can be sent to fal.ai or another compatible configured provider. <br>
Mitigation: Do not include confidential business text or personal data in prompts or reference URLs unless that third-party processing is acceptable. <br>
Risk: The fallback renderer requires an API key in config.json for provider calls. <br>
Mitigation: Protect any configured API key and avoid committing or sharing a filled config.json. <br>
Risk: Run folders can contain prompts, provider URLs, generation requests, results, and generated images. <br>
Mitigation: Review run-folder contents before sharing and avoid publishing generation metadata that includes sensitive prompt text or provider URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/billzhuang6569/zhuang-infochart-master) <br>
- [Publisher profile](https://clawhub.ai/user/billzhuang6569) <br>
- [Style catalog](artifact/references/style_catalog.md) <br>
- [Fallback image renderer](artifact/scripts/render_image.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with final English image prompts, Chinese explanations, optional shell commands, and local run-folder files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts are generated from user-provided content and selected style templates; optional image generation writes prompt, request, result, and image files into a task run folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
