## Description:

Proxy Gateway X402 enables pay-per-use HTTP proxy access for AI agents through the x402 protocol with USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kehongpeng](https://clawhub.ai/user/kehongpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route web requests through a pay-per-use proxy, configure x402 payment handling, or self-host the proxy gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad request forwarding can expose sensitive headers, bodies, or internal URLs to a proxy operator.

Mitigation: Avoid proxying secrets or internal/private URLs; self-host only in an isolated environment with SSRF protections and restrictive CORS.

Risk: Automatic wallet spending can create financial exposure if USER_EVM_PRIVATE_KEY is placed on an untrusted or public server.

Mitigation: Do not set USER_EVM_PRIVATE_KEY on public servers; use a dedicated low-balance wallet with spending limits for experiments.

Risk: Payment validation and dependency drift can affect a self-hosted payment gateway.

Mitigation: Review before deployment, add payment validation, and pin dependencies before self-hosting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kehongpeng/skills/proxy-gateway-x402)
- [x402 Protocol](https://x402.org)
- [Base Network](https://base.org)
- [Polygon Network](https://polygon.technology)
- [Proxy Gateway Documentation](https://docs.proxy.easky.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, shell, JSON, and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment headers, proxy request examples, wallet configuration notes, and self-hosting steps.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
