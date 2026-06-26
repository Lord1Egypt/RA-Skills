## Description: <br>
Use undici for HTTP requests, fetch, connection pooling, proxies, Mock testing, interceptors, caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for practical guidance on making HTTP requests with undici in Node.js, including fetch, request, streams, connection pooling, proxies, mocks, interceptors, and caching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can introduce outbound network access, proxy routing, or dispatcher changes when copied into an environment. <br>
Mitigation: Review before installing in restricted environments, prefer local dispatchers when possible, and align undici dependency use with normal pinning and audit policy. <br>
Risk: Proxy examples may encourage embedding credentials directly in code. <br>
Mitigation: Avoid hardcoding proxy credentials and manage secrets through approved environment or secret-management controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/undici) <br>
- [Connection Management: Agent / Pool / Client](references/connection.md) <br>
- [Dispatcher - Low-Level API](references/dispatcher.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may include network, proxy, dispatcher, mocking, and cache configuration patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
