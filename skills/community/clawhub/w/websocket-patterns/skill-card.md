## Description: <br>
Guides agents through WebSocket and SSE architecture decisions for transport choice, authentication, message protocols, reliability, scaling, operations, and abuse controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, review, or troubleshoot realtime systems such as dashboards, chat, collaborative editing, and notification workflows. It helps an agent structure guidance around transport choice, authentication, heartbeats, ordering, backpressure, horizontal scaling, observability, and abuse controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Realtime architecture guidance can involve security-sensitive choices for tokens, cookies, authorization, origins, and long-lived connections. <br>
Mitigation: Review recommendations against the application's threat model, require WSS, validate origins where applicable, authorize every subscription server-side, and avoid long-lived secrets in query strings. <br>
Risk: Incorrect heartbeat, reconnect, ordering, or backpressure guidance can lead to unstable production behavior under proxy timeouts, missed messages, or reconnect storms. <br>
Mitigation: Validate heartbeat intervals against proxy and load balancer timeouts, test exponential backoff with jitter, define delivery semantics, and set buffer, rate-limit, and load-shedding policies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/websocket-patterns) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with checklists, design heuristics, and implementation considerations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory workflow content only; it does not run code, request credentials, or change the user's system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
