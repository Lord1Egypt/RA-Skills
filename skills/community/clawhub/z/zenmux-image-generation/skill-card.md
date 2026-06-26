## Description: <br>
Generate images via ZenMux API (Pro/Elite). Supports Text-to-Image, Image-to-Image, and Multi-Image reference fusion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate new images, modify existing images, or combine multiple reference images through the ZenMux API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to ZenMux for cloud image generation. <br>
Mitigation: Use a revocable ZenMux API key and avoid submitting confidential, regulated, or personal images unless ZenMux policies are acceptable. <br>
Risk: The helper script writes the generated image to the configured output path. <br>
Mitigation: Choose the output path deliberately and review files before overwriting existing assets. <br>


## Reference(s): <br>
- [ZenMux Vertex AI API endpoint](https://zenmux.ai/api/vertex-ai) <br>
- [ClawHub skill page](https://clawhub.ai/dadaniya99/zenmux-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated image files are written by the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZENMUX_API_KEY and may use local reference image files.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
