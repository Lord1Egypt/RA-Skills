## Description:

Create and edit SHEIN fashion product images, model try-on visuals, colorway sets, fabric details, outfit styling and campaign-ready bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, content teams, and agents use this skill to generate and edit SHEIN-oriented fashion listing images, try-on visuals, colorway sets, fabric-detail images, outfit scenes, and campaign-ready base assets from approved garment references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected media files to AI Hive for generation.

Mitigation: Upload only approved product references and avoid private, unrelated, or sensitive files.

Risk: The skill stores an AI Hive API key under the user's home directory.

Mitigation: Use a dedicated key where possible and keep the generated config file permission-restricted.

Risk: The skill installs and uses the requests package before making API calls.

Mitigation: Install dependencies in a dedicated virtual environment from a trusted package index.

Risk: Generated fashion images can misrepresent garment structure, fit, color, material, or platform claims.

Mitigation: Review outputs against merchant-approved references and current SHEIN product and advertising requirements before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shein-ecommerce-image-generation-editing)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; runtime output may include JSON task status and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reference images and prompts to submit AI Hive image-generation tasks, then downloads results unless no-download mode is selected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
