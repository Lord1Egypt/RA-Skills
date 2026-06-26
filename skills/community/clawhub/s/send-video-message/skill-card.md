## Description: <br>
Send the user a video message with an AI avatar that speaks any text, using Runway Character API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yining1023](https://clawhub.ai/user/yining1023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send short async video updates, code review walkthroughs, deploy notifications, incident summaries, and other messages that benefit from a spoken avatar instead of plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken text, avatar images, and generated portrait prompts are sent to Runway under the user's API key. <br>
Mitigation: Use only data approved for Runway, and avoid confidential incident details, private code review content, or personal images unless Runway is approved for that data. <br>
Risk: The skill saves a reusable avatar ID in ~/.openclaw/runway-avatar.json and may incur Runway usage or billing. <br>
Mitigation: Set RUNWAY_API_SECRET securely, monitor Runway usage or billing, and delete the saved avatar config if future avatar reuse is not desired. <br>
Risk: Square and vertical output require ffmpeg, and the two crop options are mutually exclusive. <br>
Mitigation: Install ffmpeg before using --square or --vertical, and choose one output format per generated video. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yining1023/send-video-message) <br>
- [Runway API documentation](https://docs.dev.runwayml.com) <br>
- [Declared OpenClaw repository](https://github.com/runwayml/openclaw-skill-send-video-message) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated MP4 media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are saved under /tmp and emitted with a MEDIA path for attachment.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
