## Description: <br>
Manage SenseAudio realtime agent lifecycle APIs for listing agents, starting or continuing sessions, querying status, and leaving sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate SenseAudio conversational agents, manage realtime session state, handle returned room credentials, and troubleshoot lifecycle API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SenseAudio API key and returned realtime tokens that could grant access if exposed. <br>
Mitigation: Keep the API key and returned tokens server-side, avoid logging them, and discard short-lived tokens after the session ends. <br>
Risk: Stored conv_id and room_id values can be misapplied across users or sessions. <br>
Mitigation: Bind conv_id and room_id values to the correct user or session and store them in application state rather than client-side code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scikkk/realtime-agent) <br>
- [Realtime Agent Reference](references/agent.md) <br>
- [SenseAudio Homepage](https://senseaudio.cn) <br>
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key) <br>
- [List Realtime Agents API](https://api.senseaudio.cn/v1/realtime/agents) <br>
- [Invoke Realtime Session API](https://api.senseaudio.cn/v1/realtime/invoke) <br>
- [Realtime Status API](https://api.senseaudio.cn/v1/realtime/status) <br>
- [Leave Realtime Session API](https://api.senseaudio.cn/v1/realtime/leave) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API request examples and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SenseAudio API endpoint details, error handling guidance, and credential handling recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
