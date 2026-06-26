## Description: <br>
Use this skill to generate AI images using the SeaArt platform with multiple text-to-image models, custom dimensions, LoRA models, and negative prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seaartpublic](https://clawhub.ai/user/seaartpublic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images from text prompts through SeaArt, selecting supported models, aspect ratios, LoRA settings, and negative prompts as needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SeaArt browser session token stored in SEAART_TOKEN. <br>
Mitigation: Treat SEAART_TOKEN like a password, store it only in local agent configuration, and use non-printing checks instead of commands that echo the token. <br>
Risk: Prompts and generation parameters are sent to SeaArt for image generation. <br>
Mitigation: Use the skill only when the user is comfortable sharing creative prompts and generation settings with SeaArt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seaartpublic/seaart-image) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/seaartpublic) <br>
- [SeaArt platform](https://www.seaart.ai) <br>
- [SeaArt text-to-image endpoint](https://www.seaart.ai/api/v1/task/v2/text-to-img) <br>
- [SeaArt batch progress endpoint](https://www.seaart.ai/api/v1/task/batch-progress) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and returned image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SeaArt session token in SEAART_TOKEN and Python with the requests library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
