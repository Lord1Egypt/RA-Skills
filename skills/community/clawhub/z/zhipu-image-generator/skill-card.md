## Description: <br>
Generate images via BigModel APIs and send them as chat images (e.g. Feishu). Invoke when user asks to create a single picture with specific style/size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HenryBao91](https://clawhub.ai/user/HenryBao91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate a single image from a Chinese or English prompt, choosing supported BigModel/Zhipu models, dimensions, watermark behavior, and an output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation requests are sent to BigModel/Zhipu. <br>
Mitigation: Use the skill only when sharing the prompt with BigModel/Zhipu is acceptable. <br>
Risk: The skill may look for ZHIPU_API_KEY in local TOOLS.md files if the environment variable is absent. <br>
Mitigation: Set ZHIPU_API_KEY explicitly in the environment and avoid storing API keys in TOOLS.md. <br>
Risk: The output path can be chosen by the caller. <br>
Mitigation: Keep output paths inside a known workspace image directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HenryBao91/zhipu-image-generator) <br>
- [BigModel Image Generations API](https://open.bigmodel.cn/api/paas/v4/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Local image file path with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY and writes a downloaded image to the requested or generated local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
