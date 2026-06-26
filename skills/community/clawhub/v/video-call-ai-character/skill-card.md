## Description: <br>
Video Call AI Character lets an agent initiate a real-time video call with an AI avatar powered by Runway for standups, urgent alerts, check-ins, or conversations that benefit from a face-to-face format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yining1023](https://clawhub.ai/user/yining1023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to start real-time AI-avatar video calls for standups, urgent alerts, check-ins, complex explanations, or other conversations where voice, video, transcripts, and follow-up context are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video calls may process sensitive audio, video, transcripts, recordings, avatar images, and personality context through Runway. <br>
Mitigation: Use explicit opt-in for calls and recordings, avoid sensitive personal or business details in avatar personality text, and delete recordings or avatars that are no longer needed. <br>
Risk: A remote tunnel can make call links reachable outside localhost. <br>
Mitigation: Prefer localhost when possible, enable tunneling only when the user needs another device, share links only with the intended participant, and stop the server when finished. <br>
Risk: The security scan flagged unclear consent, retention, and sharing controls for transcripts and recordings. <br>
Mitigation: Confirm the user's consent before initiating calls, tell the user when a recording or transcript is produced, and follow local retention and sharing policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yining1023/video-call-ai-character) <br>
- [openclaw-video-call npm package](https://www.npmjs.com/package/openclaw-video-call) <br>
- [Runway OpenClaw skill source](https://github.com/runwayml/openclaw-skills/tree/main/video-call-ai-character) <br>
- [Runway developer documentation](https://dev.runwayml.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, HTTP API examples, call links, transcripts, and recording URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RUNWAYML_API_SECRET plus node and npm; cloudflared tunneling is optional for remote-device calls.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
