## Description: <br>
Generates professional business logo images from user descriptions using Alibaba Cloud DashScope's Qwen image model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imnull](https://clawhub.ai/user/imnull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect logo requirements, turn them into image-generation prompts, call the bundled Python script, and return generated logo image URLs or saved file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logo prompts are sent to Alibaba DashScope. <br>
Mitigation: Use a dedicated DashScope API key and avoid prompts that include confidential brand strategy, unreleased product names, or other sensitive details. <br>
Risk: The script changes saved file permissions to 644 and the containing directory to 755. <br>
Mitigation: Use a dedicated output directory and review or remove the permission-changing behavior before running it in private or shared directories. <br>
Risk: The script downloads API-returned image URLs without validating the URL first. <br>
Mitigation: Run it in a constrained environment and review the returned URL or network controls before using it with sensitive systems. <br>


## Reference(s): <br>
- [Qwen Logo Designer ClawHub page](https://clawhub.ai/imnull/qwen-logo-designer) <br>
- [DashScope multimodal generation API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image URLs or PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key; generated images are saved locally with MD5-based filenames when downloaded.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
