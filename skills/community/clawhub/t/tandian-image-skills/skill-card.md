## Description: <br>
Processes local lifestyle venue scene images by combining a user-provided scene with a preset or user-provided person reference through Replicate image editing, then upscales the result with SeedVR2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turkyden](https://clawhub.ai/user/turkyden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and operators preparing local lifestyle, restaurant, cafe, store, mall, or showroom promotional imagery use this skill to place a person reference into a venue scene and return an upscaled output image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scene images, template images, template URL content, and prompts are sent to Replicate/SeedVR2 for processing. <br>
Mitigation: Avoid sensitive, customer-identifying, proprietary, or unconsented images unless sharing them with the provider is acceptable. <br>
Risk: Generated image files are written to a user-selected or default output path. <br>
Mitigation: Confirm that the output path is writable and appropriate for the generated content before running the skill. <br>
Risk: The workflow consumes the configured Replicate account quota. <br>
Mitigation: Run only with an intended Replicate API token and monitor usage for the account used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turkyden/tandian-image-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and a generated image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Replicate API token, an accessible scene image path or URL, and a writable output path.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
