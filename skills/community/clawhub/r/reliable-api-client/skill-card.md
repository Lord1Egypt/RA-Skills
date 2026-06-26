## Description: <br>
A Node.js API client helper for endpoint failover, API-key rotation, rate limiting, retries, and circuit breakers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danihe001](https://clawhub.ai/user/danihe001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to configure and reuse a resilient Node.js API client that can route requests across multiple endpoints and keys while applying retry, timeout, rate-limit, and circuit-breaker behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests, payloads, and API keys may be sent to any configured primary or backup endpoint during retries or failover. <br>
Mitigation: Configure only trusted endpoints and avoid hard-coding production keys in shared code. <br>
Risk: A background health-check interval can keep running longer than intended. <br>
Mitigation: Stop or disable the health-check interval when the client is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danihe001/reliable-api-client) <br>
- [Project homepage](https://github.com/tvvshow/openclaw-evomap) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript usage examples and a Node.js source file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper sends requests to user-configured API endpoints and can use user-provided API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
