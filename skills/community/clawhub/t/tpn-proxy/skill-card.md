## Description: <br>
Make web requests through decentralized SOCKS5 proxies via the Tao Private Network (TPN). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[actuallymentor](https://clawhub.ai/user/actuallymentor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate short-lived SOCKS5 proxy credentials, route validated public web requests through TPN, check country-specific access, or use API-key and x402 payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts TPN, can consume proxy credits, and routes selected public web requests through third-party proxy nodes. <br>
Mitigation: Install only when that traffic path and credit use are acceptable, and keep requests limited to validated public destinations. <br>
Risk: The skill depends on TPN_API_KEY and may display live SOCKS5 usernames and passwords in agent responses. <br>
Mitigation: Configure TPN_API_KEY through a secure environment or secret setting, do not paste it into chat, and treat generated proxy credentials as temporary secrets. <br>
Risk: Fetching user-specified URLs through a proxy can be unsafe if destination validation is skipped. <br>
Mitigation: Require HTTP or HTTPS URLs, reject raw IPs and internal hostnames, verify public DNS resolution, and quote proxy and URL arguments when shell commands are unavoidable. <br>


## Reference(s): <br>
- [TPN API Code Examples](references/api-examples.md) <br>
- [TPN x402 Code Examples](references/x402-examples.md) <br>
- [TPN Security Assessment](references/security-assessment.md) <br>
- [TPN API Documentation](https://api.taoprivatenetwork.com/api-docs/) <br>
- [TPN OpenAPI Specification](https://api.taoprivatenetwork.com/api-docs/openapi.json) <br>
- [x402 Protocol](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with proxy configuration blocks, SOCKS5 URIs, curl examples, and fetched response text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include short-lived proxy credentials, credit usage details, expiration timestamps, and public web response content.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
