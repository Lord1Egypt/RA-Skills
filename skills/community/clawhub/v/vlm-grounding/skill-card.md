## Description: <br>
Uses GLM-4.7V multimodal grounding to help detect and locate objects, text, UI elements, and regions in images with bounding-box outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qijimrc](https://clawhub.ai/user/qijimrc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user asks to find, locate, detect, or ground specific visual targets in an image. It guides model calls, bounding-box parsing, and visualization of detected regions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an unrelated captured API/chat log containing user image data and internal OpenClaw context. <br>
Mitigation: Review or remove artifact/ssssss.json before installing or distributing the skill. <br>
Risk: The skill sends images and prompts to a GLM/VLM endpoint, which may expose sensitive image content if the endpoint is not trusted. <br>
Mitigation: Use only trusted model endpoints and avoid sensitive images unless that endpoint is approved for the data. <br>
Risk: The package relies on declared configuration paths and helper modules that are not fully represented in the artifact. <br>
Mitigation: Ask the publisher to ship a minimal package with the required helper modules and explicit configuration paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qijimrc/vlm-grounding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with Python snippets and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of annotated image files with bounding boxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
