## Description: <br>
Generates Wan 2.7 text-to-video requests on RunComfy through the local RunComfy CLI, with guidance for audio-driven lip-sync, prompt expansion, duration, resolution, aspect ratio, and routing to related video models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and agent operators use this skill to decide when Wan 2.7 is appropriate and to invoke RunComfy text-to-video generation with valid inputs. It is especially suited to short clips requiring custom audio-driven lip-sync, multi-reference motion control, smooth transitions, or negative-prompted cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on the local RunComfy CLI and a RunComfy token. <br>
Mitigation: Verify the CLI package provenance before installation and keep RUNCOMFY_TOKEN private. <br>
Risk: Prompts, audio, and media URLs are submitted to RunComfy's hosted service for generation. <br>
Mitigation: Only submit content the user is comfortable sending to RunComfy. <br>
Risk: Generated outputs are downloaded into a user-selected output directory. <br>
Mitigation: Choose an appropriate output directory and review generated files before reuse. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kalvinrv/wan-2-7) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-2-7) <br>
- [Wan 2.7 text-to-video model page](https://www.runcomfy.com/models/wan-ai/wan-2-7/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-2-7) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-2-7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with RunComfy CLI commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of an output directory where the RunComfy CLI may save generated video files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
