## Description: <br>
Extend or continue an existing video clip on RunComfy via the runcomfy CLI by routing to Google Veo 3-1 extend-video or fast/extend-video endpoints with a source video and continuation prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to extend a user-provided video clip or build a longer chained video narrative through RunComfy's Veo 3-1 video continuation endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected video URL and continuation prompt are sent to RunComfy for external video generation. <br>
Mitigation: Use only videos the user explicitly provides and avoid submitting sensitive videos unless the user accepts RunComfy processing. <br>
Risk: RunComfy tokens can authorize paid model runs if exposed. <br>
Mitigation: Protect RUNCOMFY_TOKEN and local token files, and never echo tokens into prompts, logs, or generated command output. <br>
Risk: Chained video extensions can consume credits and produce large files. <br>
Mitigation: Confirm expected cost before multi-step extensions and keep generated downloads within the CLI's file-size limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kalvinrv/video-extend) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [Veo 3-1 Extend Video](https://www.runcomfy.com/models/google-deepmind/veo-3-1/extend-video?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend) <br>
- [Veo 3-1 Fast Extend Video](https://www.runcomfy.com/models/google-deepmind/veo-3-1/fast/extend-video?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend) <br>
- [Veo 3-1 Collection](https://www.runcomfy.com/models/collections/veo-3?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend) <br>
- [RunComfy CLI Docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend) <br>
- [RunComfy CLI Troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON CLI input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI, a RunComfy token, and a user-provided source video URL; generated video files are downloaded to the selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
