## Description:

TPN Proxy lets agents generate and use short-lived SOCKS5 proxies through Tao Private Network for anonymous or geography-specific web requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[actuallymentor](https://clawhub.ai/user/actuallymentor)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to lease SOCKS5 proxy credentials, fetch public URLs through a proxy, inspect available proxy countries, and use API-key or x402 payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived API keys could be exposed if pasted into chat or browser-side code.

Mitigation: Store TPN_API_KEY in a platform secret manager or environment variable and never echo, log, or display the key value.

Risk: x402 payment flows can authorize funds to the wrong recipient, network, token, amount, or spending limit.

Mitigation: Review payment details in the wallet before approving any transaction and use the documented x402 libraries for signing.

Risk: Proxy URL fetching may send request data through third-party proxy infrastructure.

Mitigation: Use the skill only for public URLs that are acceptable to route through TPN/proxy infrastructure.

Risk: Constructing shell commands from user-supplied proxy parameters or URLs can introduce injection risk.

Mitigation: Validate country codes, durations, formats, connection types, and URLs before command construction; prefer built-in HTTP tooling for URL fetches.

## Reference(s):

- [TPN Proxy on ClawHub](https://clawhub.ai/actuallymentor/skills/tpn-proxy)
- [TPN API](https://api.taoprivatenetwork.com)
- [TPN Getting Started](https://api.taoprivatenetwork.com/docs/getting-started/)
- [TPN API Documentation](https://api.taoprivatenetwork.com/api-docs/)
- [TPN OpenAPI Specification](https://api.taoprivatenetwork.com/api-docs/openapi.json)
- [TPN LLM Reference](https://api.taoprivatenetwork.com/docs/llms-full.txt)
- [x402 Protocol](https://www.x402.org)
- [TPN API Code Examples](references/api-examples.md)
- [TPN Security Assessment](references/security-assessment.md)
- [TPN x402 Code Examples](references/x402-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with proxy credentials, API results, and code or shell examples when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short-lived SOCKS5 credentials, URLs, API status details, and validated request parameters.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
