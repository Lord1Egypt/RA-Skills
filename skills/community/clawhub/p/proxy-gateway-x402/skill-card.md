## Description: <br>
Proxy Gateway X402 provides pay-per-use HTTP proxy access for agents using x402-style USDC payments and optional self-hosted server components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kehongpeng](https://clawhub.ai/user/kehongpeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to route agent HTTP requests through a paid proxy or to self-host a gateway with x402/USDC payment handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted proxy can see proxied URLs, headers, request bodies, and responses. <br>
Mitigation: Do not send bearer tokens, passwords, private keys, personal data, or internal network URLs through the hosted service; self-host when privacy is required. <br>
Risk: Automatic wallet-payment flows can expose or misuse funds if configured with sensitive wallets. <br>
Mitigation: Use a dedicated low-balance wallet, avoid exposing USER_EVM_PRIVATE_KEY on public servers, and review payment verification before production use. <br>
Risk: The release was flagged suspicious by the authoritative security scan because it combines arbitrary traffic forwarding with wallet-payment automation and weak safety controls. <br>
Mitigation: Review the scan guidance, open-proxy controls, and payment verification behavior before installing or operating the service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kehongpeng/proxy-gateway-x402) <br>
- [X402 Integration Guide](docs/X402_INTEGRATION.md) <br>
- [x402 Protocol](https://x402.org) <br>
- [Proxy Gateway Service](https://proxy.easky.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, environment variable setup, and self-hosting commands.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
