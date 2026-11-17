## Description:

Video call the user with a real-time AI avatar powered by Runway for standups, urgent alerts, check-ins, or any conversation that benefits from face-to-face interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yining1023](https://clawhub.ai/user/yining1023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to let an agent start a real-time video call through a Runway-powered avatar, share urgent updates or conversational check-ins, and then use the transcript and recording for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an npm-hosted local service that the security evidence describes as unpinned.

Mitigation: Pin the npm package version, review its dependency tree, and audit the installed runtime before enabling the skill.

Risk: Avatar images, personality text, call audio/video, transcripts, and recordings may be processed by Runway.

Mitigation: Use the skill only with explicit user consent, minimize personal context in prompts, and avoid sending sensitive images or conversations unless approved.

Risk: Remote call access through cloudflared can expose the local call service beyond localhost.

Mitigation: Keep cloudflared disabled unless remote-device calling is required, and share tunnel URLs only with the intended recipient.

Risk: Call recordings and transcripts can contain sensitive user decisions or instructions.

Mitigation: Require consent before recording, downloading, forwarding, or retaining call artifacts, and review transcripts before acting on consequential requests.

## Reference(s):

- [Runway Developer API](https://dev.runwayml.com)
- [openclaw-video-call npm package](https://www.npmjs.com/package/openclaw-video-call)
- [OpenClaw video-call-ai-character source](https://github.com/runwayml/openclaw-skills/tree/main/video-call-ai-character)
- [ClawHub skill page](https://clawhub.ai/yining1023/skills/video-call-ai-character)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown instructions with shell commands, HTTP API examples, and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local npm service, RUNWAYML_API_SECRET, and optional cloudflared tunneling for calls from another device.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
