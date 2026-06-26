## Description: <br>
Uses the Volcengine ARK API for image understanding, image description, visual question answering, and image analysis over local image paths, image URLs, or base64 images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-dust](https://clawhub.ai/user/big-dust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to answer questions about images, describe image contents, and analyze information in local files, URLs, or base64-encoded images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image content and prompts are sent to the external Volcengine ARK service during use. <br>
Mitigation: Use the skill only when cloud-based ARK processing is intended, and avoid submitting private photos, IDs, screenshots, confidential documents, or regulated data unless that external processing is acceptable. <br>
Risk: The required ARK_API_KEY grants access to the external image-analysis provider. <br>
Mitigation: Use a dedicated API key with appropriate scope and rotate or revoke it according to the deployment's credential policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/big-dust/volc-vision) <br>
- [Publisher profile](https://clawhub.ai/user/big-dust) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text returned by the command-line skill, with optional model status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and ARK_API_KEY; VISION_MODEL can optionally select a supported vision model.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
