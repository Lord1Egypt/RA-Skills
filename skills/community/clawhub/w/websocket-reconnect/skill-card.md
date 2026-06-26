## Description: <br>
WebSocket connection management with exponential backoff + jitter retry, heartbeat detection, and circuit breaker pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwe123sddfsdfs](https://clawhub.ai/user/qwe123sddfsdfs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add reliable WebSocket client behavior, including reconnect retry, heartbeat detection, circuit breaker handling, and connection status monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WebSocket traffic may expose messages or credentials if the skill is configured with untrusted endpoints. <br>
Mitigation: Use only trusted WebSocket endpoints and avoid sending secrets to servers you do not control or trust. <br>
Risk: The skill depends on the ws package from the npm ecosystem. <br>
Mitigation: Install dependencies from a trusted npm registry or mirror and review lockfile integrity before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qwe123sddfsdfs/websocket-reconnect) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with JavaScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WebSocket client implementation guidance for Node.js and browser-style usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
