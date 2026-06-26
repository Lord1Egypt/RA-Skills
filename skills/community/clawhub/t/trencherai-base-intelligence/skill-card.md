## Description: <br>
TrencherAI provides paid x402 API guidance for scoring Base chain tokens with smart-money, launchpad, social, deployer, pattern, and liquidity signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soynull](https://clawhub.ai/user/soynull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to query TrencherAI's paid Base-chain endpoints for token screening, hot-token feeds, and smart-money activity. Outputs can support monitoring and trading workflows, but financial actions should not rely solely on these scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: x402 requests spend USDC from the caller's wallet. <br>
Mitigation: Use a dedicated low-balance wallet, strict per-call spending limits, and confirmation controls before enabling automated requests. <br>
Risk: Automated trading decisions can over-rely on token scores. <br>
Mitigation: Treat scores as decision support only and require independent review or additional safeguards before trades execute. <br>
Risk: Payments could be sent to an unexpected recipient if endpoint metadata is not checked. <br>
Mitigation: Verify the x402 pay-to address and Base network details before allowing the client to pay. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soynull/trencherai-base-intelligence) <br>
- [TrencherAI Website](https://aitrencher.xyz) <br>
- [x402 Discovery](https://api.aitrencher.xyz/.well-known/x402.json) <br>
- [ERC-8004 Agent Registry](https://www.8004scan.io/agents/base/29167) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples, client-side x402 payment setup, and JSON response field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses paid USDC requests on Base through an x402-compatible client; no TrencherAI-side credentials are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
