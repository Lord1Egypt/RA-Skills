## Description: <br>
Jimeng AI Image Generator calls the Volcengine Jimeng API to generate images and videos from prompts and includes prompt templates for ecommerce, social media, commercial design, and video scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate Jimeng/Volcengine images or videos from prompts, query generation tasks, and reuse prompt templates for marketing, social media, and design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation requests are sent to Volcengine/Jimeng. <br>
Mitigation: Avoid sending secrets, regulated data, or confidential material in prompts unless approved for that external service. <br>
Risk: The skill requires Jimeng/Volcengine credentials and can consume quota or paid capacity. <br>
Mitigation: Use a scoped key where possible, store it only in the expected secrets manager, and monitor quota and billing. <br>
Risk: Generated image data may be written to local output paths. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important files. <br>
Risk: The release security summary notes that metadata does not explicitly declare network/API use. <br>
Mitigation: Confirm that external API access to Volcengine is acceptable before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luis1213899/xingxiaolu-jimeng) <br>
- [Prompt Template Library](references/prompts-templates.md) <br>
- [Prompt Template Source Article](https://www.tahou.com/article/203607417559502853) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Command output with task IDs, MEDIA_URL values, generated image files, and video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write image files to the requested output path or the skill directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
