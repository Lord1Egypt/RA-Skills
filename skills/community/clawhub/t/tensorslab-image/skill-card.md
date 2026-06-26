## Description: <br>
Generate and edit images using TensorsLab's AI models with text-to-image, image-to-image, avatar generation, watermark removal, object erasure, face replacement, prompt enhancement, progress tracking, and local file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate images, transform source images, and run common image-editing workflows through TensorsLab's API. It supports prompt enhancement, asynchronous task tracking, and saving completed outputs locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watermark removal guidance could be used on images where the user lacks rights. <br>
Mitigation: Use the skill only on images the user owns or is authorized to modify, and avoid removing third-party attribution or rights markings. <br>
Risk: Face replacement and avatar workflows could be used to impersonate people or edit faces without consent. <br>
Mitigation: Require consent for identifiable people and avoid prompts intended to deceive viewers about identity or authenticity. <br>
Risk: Prompts, source images, and the API key are sent to TensorsLab's external API. <br>
Mitigation: Avoid uploading sensitive photos, confidential prompts, or regulated data unless the user accepts TensorsLab as a trusted processor. <br>


## Reference(s): <br>
- [TensorsLab Image API Reference](references/api_reference.md) <br>
- [TensorsLab Image Generation Scenarios](references/scenarios.md) <br>
- [TensorsLab Console](https://tensorai.tensorslab.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/bob5-tensorslab/tensorslab-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TENSORSLAB_API_KEY; generated or edited images are saved to tensorslab_output/ unless a custom output directory is provided.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
