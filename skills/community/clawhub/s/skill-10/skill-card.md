## Description: <br>
Edit Clawra's reference image with Grok Imagine (xAI Aurora) and send selfies to messaging channels via OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhi8145](https://clawhub.ai/user/wangzhi8145) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to generate context-specific Clawra selfie images and send them to selected messaging channels. It supports prompt collection, image editing through fal.ai, and delivery through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated media can be sent to real messaging channels. <br>
Mitigation: Confirm the image, caption, platform, and target channel before sending. <br>
Risk: The workflow sends prompts and generated images to fal.ai and then through OpenClaw to selected messaging platforms. <br>
Mitigation: Use the skill only when that data sharing is acceptable for the content and workspace. <br>
Risk: The release asks for credentials and broad execution permissions beyond what its registry metadata clearly declares. <br>
Mitigation: Provide only the required FAL API key and OpenClaw token, and restrict npm, npx, file access, and web permissions where the agent environment supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangzhi8145/skill-10) <br>
- [Clawra reference image](https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png) <br>
- [fal.ai API key dashboard](https://fal.ai/dashboard/keys) <br>
- [Grok Imagine Edit API endpoint](https://fal.run/xai/grok-imagine-image/edit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with bash and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompts, API request examples, image URLs, and messaging send commands; requires user confirmation of destination channel and generated media before sending.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
