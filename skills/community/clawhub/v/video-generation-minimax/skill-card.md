## Description: <br>
Creates videos with the MiniMax video generation API from text prompts, image prompts, start/end frames, or subject reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbos1314](https://clawhub.ai/user/xbos1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit MiniMax video generation jobs, monitor asynchronous completion, and save the resulting video file for review or downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and image URLs, including face photos in subject-reference mode, are sent to the MiniMax third-party service. <br>
Mitigation: Use only prompts and media that are appropriate to share with MiniMax, and avoid sensitive or non-consensual face images. <br>
Risk: The skill downloads provider-returned video files into the workspace. <br>
Mitigation: Review generated videos before use and clean up workspace files when they are no longer needed. <br>
Risk: The MiniMax API key is required for operation. <br>
Mitigation: Store MINIMAX_API_KEY as a protected environment variable and avoid placing it in prompts, logs, or committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xbos1314/video-generation-minimax) <br>
- [MiniMax API documentation](https://platform.minimaxi.com/docs/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, API Calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and python3; uses prompt, mode, image URL inputs, duration, resolution, and output filename parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
