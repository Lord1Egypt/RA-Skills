## Description: <br>
Implement reliable WebSocket connections with proper reconnection, heartbeats, and scaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design and review WebSocket clients and services with reconnection, heartbeat, authentication, proxy, scaling, and message-handling practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive tokens in WebSocket URLs may be captured in access logs. <br>
Mitigation: Prefer secure authentication patterns and avoid placing sensitive tokens in URL query strings. <br>
Risk: WebSocket services can accept unwanted cross-site or abusive client traffic if origins and messages are not controlled. <br>
Mitigation: Validate WebSocket origins, rate-limit clients, and validate every client message. <br>
Risk: Connections can appear healthy after silent drops, causing messages to fail or queue unexpectedly. <br>
Mitigation: Use application-level heartbeats, reconnect on missed pongs, and apply exponential backoff with jitter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/websocket) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Code snippets] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
