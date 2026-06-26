## Description: <br>
Guides an agent through RunComfy-based video outpainting workflows that extend a video's spatial canvas, change aspect ratio, and preserve the central action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and video production teams use this skill to prepare prompts and RunComfy CLI commands for spatially extending videos, converting aspect ratios, and selecting higher-quality ComfyUI outpainting workflows when seam quality matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive videos may be processed by an external RunComfy service. <br>
Mitigation: Use only videos appropriate for the connected RunComfy account and avoid sensitive inputs unless the user understands the service boundary and token being used. <br>
Risk: Prompt-shaped outpainting can vary in seam quality or alter the central subject. <br>
Mitigation: Use preservation language in prompts, review generated outputs before use, and choose dedicated ComfyUI outpainting workflows for hero-grade seam quality. <br>
Risk: The skill requires a local RunComfy CLI and account token. <br>
Mitigation: Install the CLI through a verified package manager, keep account tokens protected, and prefer environment variables for CI or container use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kalvinrv/video-outpainting) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting) <br>
- [Wan 2-7 Edit-Video Model](https://www.runcomfy.com/models/wan-ai/wan-2-7/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting) <br>
- [LTX 2-3 Outpainting in ComfyUI](https://www.runcomfy.com/comfyui-workflows/ltx-2-3-outpainting-in-comfyui-spatial-frame-expansion-workflow?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting) <br>
- [RunComfy CLI Troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=video-outpainting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a RunComfy account token and produces instructions for writing generated video outputs to a local output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
