## Description:

Start a video call with a real-time AI avatar using the Runway Characters API. The agent sends the user a call invite link for standups, urgent alerts, check-ins, or any conversation that's better face-to-face.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yining1023](https://clawhub.ai/user/yining1023)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to invite a user into a real-time avatar video call for urgent alerts, standups, decision points, complex explanations, or status updates. After the call ends, the agent can use the transcript and recording link to summarize the discussion and take follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm runtime.

Mitigation: Review and pin the npm package version where possible before installation or repeated use.

Risk: Avatar images, personality prompts, call audio/video, transcripts, and recordings may be sent to Runway.

Mitigation: Use a narrowly scoped Runway API key, avoid sensitive user context in persistent avatar prompts, and share only data users expect to provide.

Risk: Video calls may create transcripts and recordings involving sensitive user conversations.

Mitigation: Get clear user consent before recording or transcribing calls and review generated follow-up actions before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yining1023/skills/video-call-agent)
- [Runway Developer Portal](https://dev.runwayml.com)
- [openclaw-video-call npm Package](https://www.npmjs.com/package/openclaw-video-call)
- [openclaw-skills Repository](https://github.com/runwayml/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, API endpoint references, call invite links, transcript data, and recording URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, RUNWAYML_API_SECRET, and the openclaw-video-call runtime; optional cloudflared tunneling enables calls on other devices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
