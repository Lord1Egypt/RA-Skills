## Description: <br>
Access Xona's paid x402 APIs for design research, image and video generation, X news extraction, and PumpFun token intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xona-labs](https://clawhub.ai/user/xona-labs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to call Xona's paid creative and market-intelligence APIs for design research, media generation, X news drafts, and PumpFun token trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-backed paid API calls can spend funds with weak endpoint and consent controls. <br>
Mitigation: Use a dedicated low-balance wallet, verify endpoints before use, and require explicit approval for each paid call. <br>
Risk: Broad or repeated requests can increase spend and exposure before endpoint controls are reviewed. <br>
Mitigation: Avoid broad or repeated requests until an api.xona-agent.com allowlist and per-call payment confirmation are enforced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xona-labs/x402-creative-resources) <br>
- [Xona x402 resource discovery](https://api.xona-agent.com/x402-resources) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated media URLs, news summaries, tweet drafts, token intelligence, and payment-backed API call results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
