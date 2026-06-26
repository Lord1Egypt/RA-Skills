## Description: <br>
Generate and edit images with TensorsLab AI models for text-to-image, image-to-image, avatar generation, watermark removal, object erasure, face replacement, and general image editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to generate or transform images through TensorsLab's API, including text-to-image, image-to-image, and guided editing workflows. Use requires a TENSORSLAB_API_KEY and may spend account credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected source images are sent to TensorsLab and API use may spend account credits. <br>
Mitigation: Use only approved prompts and images, configure the TENSORSLAB_API_KEY intentionally, and monitor credit usage before running generation or editing jobs. <br>
Risk: Watermark-removal and face-replacement workflows can be misused on content the user does not own or to create deceptive media. <br>
Mitigation: Use these workflows only with owned content, explicit permission from depicted people, and a review process that rejects impersonation or deceptive outputs. <br>
Risk: The server security verdict is suspicious and calls for human review before installation. <br>
Mitigation: Review the skill behavior and security guidance before deployment, with particular attention to watermark-removal and face-replacement scenarios. <br>


## Reference(s): <br>
- [TensorsLab Image Skill](https://clawhub.ai/bob5-tensorslab/tl-image) <br>
- [TensorsLab Image API Reference](references/api_reference.md) <br>
- [TensorsLab Image Generation Scenarios](references/scenarios.md) <br>
- [TensorsLab API Base URL](https://api.tensorslab.com) <br>
- [TensorsLab Console](https://tensorai.tensorslab.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and locally saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are downloaded to ./tensorslab_output/ or a user-specified output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
