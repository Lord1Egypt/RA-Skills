## Description: <br>
Zoom RTMS Meeting Assistant — start on-demand to capture meeting audio, video, transcript, screenshare, and chat via Zoom Real-Time Media Streams. Handles meeting.rtms_started and meeting.rtms_stopped webhook events. Provides AI-powered dialog suggestions, sentiment analysis, and live summaries with WhatsApp notifications. Use when a Zoom RTMS webhook fires or the user asks to record/analyze a meeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanchunsiong](https://clawhub.ai/user/tanchunsiong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and meeting operations teams use this skill to run a Zoom RTMS webhook service that captures meeting media and generates transcripts, summaries, dialog suggestions, and sentiment analysis. It is intended for environments where participants understand and consent to recording and AI analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive meeting recordings, transcripts, chat, summaries, and participant-derived analysis. <br>
Mitigation: Use it only where all participants understand and consent to recording and AI analysis, and define retention, deletion, and access controls before real meetings are processed. <br>
Risk: Webhook and notification-control endpoints can expose meeting data or controls if deployed broadly. <br>
Mitigation: Place the webhook behind authentication or a trusted forwarding layer, verify Zoom webhook signatures, restrict the notification toggle endpoint, and avoid public exposure except where required and controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanchunsiong/zoom-meeting-assistance-with-rtms-unofficial-community-skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ngrok unofficial webhook skill](https://github.com/tanchunsiong/ngrok-unofficial-webhook-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON analysis files, transcript files, media files, and generated meeting summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces meeting recordings, transcripts, chat logs, AI summaries, dialog suggestions, sentiment JSON, screenshare PDFs, and converted audio/video artifacts.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
