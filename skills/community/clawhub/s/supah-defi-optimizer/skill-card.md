## Description: <br>
DeFi yield optimization, impermanent loss tracking, and portfolio management for Base blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query SUPAH's paid DeFi service for Base wallet positions, APY comparisons, impermanent loss calculations, and rebalancing suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends wallet or liquidity-position identifiers to a remote DeFi service. <br>
Mitigation: Use only wallet or position identifiers you are comfortable sharing with SUPAH and its data providers. <br>
Risk: Calls may trigger automatic x402 USDC charges. <br>
Mitigation: Use a low-limit payment wallet or spending cap and verify each charge before execution. <br>
Risk: SUPAH_API_BASE can redirect requests to an alternate endpoint. <br>
Mitigation: Leave SUPAH_API_BASE unset unless you intentionally trust the alternate endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supah-based/supah-defi-optimizer) <br>
- [SUPAH website](https://supah.ai) <br>
- [SUPAH API endpoint](https://api.supah.ai) <br>
- [x402 protocol](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and CLI JSON responses from the SUPAH API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, outbound access to api.supah.ai, and an x402-compatible payment flow using USDC on Base.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
