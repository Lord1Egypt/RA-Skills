## Description: <br>
Use GLM-4.7V's multimodal grounding capability to detect and locate objects, text, UI elements, and regions in images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qijimrc](https://clawhub.ai/user/qijimrc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send image-and-prompt grounding requests to a GLM-4.7V-compatible model endpoint, parse normalized bounding boxes, and visualize labeled boxes on the source image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated captured OpenClaw chat/API log with system prompts, tool definitions, headers, user conversation content, and a large base64 duplicate. <br>
Mitigation: Remove ssssss.json from the release package and review packaged files for private or irrelevant data before installation. <br>
Risk: The workflow sends images and prompts to a model endpoint and documents proxy bypass behavior for internal hosts. <br>
Mitigation: Use only approved model endpoints, document image data flow, and avoid sensitive images unless the endpoint and network path are approved. <br>
Risk: The skill references helper modules and local model configuration that are not bundled or pinned in the artifact. <br>
Mitigation: Include or pin the required helper modules and document the expected local model configuration before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python code examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces model-call guidance, bounding-box parsing steps, and image annotation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
