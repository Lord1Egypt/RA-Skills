## Description:

Manage SenseAudio realtime agents by listing agents, starting or continuing sessions, querying status, and leaving sessions with credential-aware error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate an agent with SenseAudio realtime Agent lifecycle APIs, including agent discovery, session invocation or continuation, status checks, and session termination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SENSEAUDIO_API_KEY and returned realtime tokens can grant access if exposed.

Mitigation: Keep API keys and realtime tokens out of logs, URLs, and client-side code; discard short-lived tokens after the session ends.

Risk: Session identifiers such as conv_id and room_id can be confused or overexposed.

Mitigation: Persist conv_id and room_id separately in server-side application state and store only the identifiers needed for continuity.

## Reference(s):

- [Realtime Agent Reference](references/agent.md)
- [SenseAudio](https://senseaudio.cn)
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/realtime-agent)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with API request examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; returned realtime tokens should not be logged, embedded in URLs, or placed in client-side code.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
