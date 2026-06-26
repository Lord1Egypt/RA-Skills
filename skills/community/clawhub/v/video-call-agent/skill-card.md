## Description: <br>
The skill starts a video call with a real-time AI avatar using the Runway Characters API and returns a call link, transcript, and recording for agent follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yining1023](https://clawhub.ai/user/yining1023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to initiate live video check-ins, urgent alerts, standups, or complex explanations with a real-time avatar. After the call, the transcript and recording support follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calls, transcripts, recordings, avatar images, and personality prompts may contain sensitive data shared with external services. <br>
Mitigation: Avoid secrets, unnecessary personal details, private project data, and biometric face images unless needed; share recordings or detailed summaries only with user approval. <br>
Risk: Remote call links and tunnels can expose the local call experience beyond localhost. <br>
Mitigation: Use cloudflared only when required for another device, stop the local server after use, and avoid posting call links in broad channels. <br>
Risk: Stored avatars and reusable personality prompts may preserve sensitive identity or user-context details. <br>
Mitigation: Keep avatar personality text minimal, reuse only approved avatar IDs, and delete unused avatars when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yining1023/video-call-agent) <br>
- [openclaw-video-call npm package](https://www.npmjs.com/package/openclaw-video-call) <br>
- [OpenClaw skills repository](https://github.com/runwayml/openclaw-skills) <br>
- [Runway developer documentation](https://dev.runwayml.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, HTTP API examples, JSON request bodies, call links, transcripts, and recording URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RUNWAYML_API_SECRET, node, npm, a local video-call server, and optional cloudflared tunneling for remote devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
