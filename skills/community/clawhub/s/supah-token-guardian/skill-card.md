## Description: <br>
Pre-trade token safety scanner for 21+ EVM chains. 6-layer deep scan: contract safety, liquidity health, deployer profiling, holder distribution, trading patterns, social signals. Returns Guardian Score (0-100) with BUY/CAUTION/AVOID verdict. x402 USDC micropayments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request pre-trade token safety reports for EVM token contracts before deciding whether to buy or avoid a token. It returns a Guardian Score, verdict, risk signals, positive signals, and a local JSON result file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each scan can make an outbound token-scan request and spend 0.08 USDC through x402. <br>
Mitigation: Require explicit user confirmation before paid scans and ensure the agent wallet has an approved USDC spending posture on Base. <br>
Risk: SUPAH_API_BASE can redirect scans to a replacement endpoint. <br>
Mitigation: Leave SUPAH_API_BASE unset unless the replacement endpoint is trusted and reviewed. <br>
Risk: The skill writes scan results to /tmp/guardian-result.json, which may be visible or overwritten on shared systems. <br>
Mitigation: Treat the local result file as sensitive scan output and remove or relocate it when shared-machine exposure matters. <br>


## Reference(s): <br>
- [Supported Chains](references/supported-chains.md) <br>
- [x402 Protocol](https://www.x402.org) <br>
- [SUPAH API](https://api.supah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Files] <br>
**Output Format:** [Markdown-style terminal report with a JSON result file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and Node.js, calls api.supah.ai by default, and writes scan output to /tmp/guardian-result.json.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
