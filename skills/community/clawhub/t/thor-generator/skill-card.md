## Description: <br>
Generate high-quality images locally using the ComfyUI Thor pipeline from user-provided text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thortheai1-hash](https://clawhub.ai/user/thortheai1-hash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn text prompts into local image files through an existing ComfyUI Thor setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to run a local shell command with user prompt text interpolated into the command. <br>
Mitigation: Install only after trusting the local ~/ComfyUI setup and inspecting thor_generate_image.py; avoid arbitrary or untrusted prompt text unless argument passing, path validation, and confirmation are added. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thortheai1-hash/thor-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files] <br>
**Output Format:** [Shell command execution that produces a local image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local ~/ComfyUI environment and thor_generate_image.py; generated images are saved to ~/Desktop/bring_img.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
