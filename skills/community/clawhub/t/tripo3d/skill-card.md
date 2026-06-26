## Description: <br>
Tripo3D AI 3D model generation. Use when generating 3D models from text prompts or images via the Tripo3D API. Supports Text-to-3D, Image-to-3D, Multiview-to-3D, model refinement, polling, and batch generation. Triggered by requests like "generate a 3D model", "text to 3D", "image to 3D", "photo to 3D", "create 3D from photo", or when the user provides a Tripo3D API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardcoder849](https://clawhub.ai/user/richardcoder849) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and 3D content creators use this skill to generate, refine, poll, and download Tripo3D models from text prompts, single images, or multiview image sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, and generated task data are sent to the external Tripo3D service. <br>
Mitigation: Avoid sending sensitive personal, proprietary, or regulated images and prompts unless the user's environment and Tripo3D account terms permit it. <br>
Risk: The skill requires a Tripo3D API key and includes command examples that use authorization headers. <br>
Mitigation: Store the API key in the TRIPO3D_API_KEY environment variable and do not paste secrets into chat, source files, or saved scripts. <br>
Risk: Proxy and download commands can affect network routing or write files locally. <br>
Mitigation: Review PowerShell proxy and download commands before running them, and choose explicit output paths for downloaded model files. <br>


## Reference(s): <br>
- [Tripo3D Platform](https://platform.tripo3d.ai) <br>
- [Tripo3D OpenAPI Base URL](https://api.tripo3d.ai/v2/openapi) <br>
- [ClawHub Skill Page](https://clawhub.ai/richardcoder849/tripo3d) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated task IDs, model download URLs, preview image URLs, and local GLB or FBX files returned by Tripo3D.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
