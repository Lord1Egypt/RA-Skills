## Description: <br>
Creates hand-drawn illustration prompts and generated image assets in multiple sketch, watercolor, vector, doodle infographic, and technical diagram styles, with optional delivery through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to turn article outlines, product explanations, process descriptions, and educational concepts into concise illustration plans, prompt packs, and generated hand-drawn images for presentations, tutorials, knowledge cards, and infographics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated images may be processed by external image generation services. <br>
Mitigation: Avoid sensitive or proprietary content unless the configured image API provider and account terms are acceptable. <br>
Risk: The scripts read shared local credentials for image generation and Feishu delivery. <br>
Mitigation: Review credential sources before use, prefer scoped credentials, and rotate any exposed or unintended keys. <br>
Risk: Generated images can be sent to a default hardcoded Feishu recipient. <br>
Mitigation: Review or change the Feishu open_id in scripts/send_to_feishu.sh before running delivery commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dadaniya99/sketch-illustration) <br>
- [Style Reference](references/styles.md) <br>
- [Prompt Guide](references/prompt-guide.md) <br>
- [Image Assistant Workflow](references/image-assistant-workflow.md) <br>
- [API Configuration](references/api-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image files] <br>
**Output Format:** [Markdown guidance with prompt blocks, JSONL request examples, shell commands, and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are written to local files and may be sent through Feishu when the delivery script is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
