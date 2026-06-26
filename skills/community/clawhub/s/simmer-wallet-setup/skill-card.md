## Description: <br>
Self-custody wallet setup for Simmer agents choosing OWS, an external raw key, or an existing dashboard-registered agent for a local runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to configure Simmer self-custody wallet access, API keys, approvals, and local signing paths for Polymarket or Kalshi agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive wallet credentials, including SIMMER_API_KEY and optional private keys. <br>
Mitigation: Follow the documented secret-handling guidance, avoid clipboard-based key piping, and store wallet material only in the intended local environment or encrypted OWS vault. <br>
Risk: Wallet approvals, activation, wrapping, and trading configuration can affect real funds. <br>
Mitigation: Run setup only for intended Simmer self-custody wallets, verify commands and package sources before execution, and confirm approvals and balances before trading. <br>
Risk: Using the wrong wallet path or chain can leave the agent unable to trade or showing unexpected balances. <br>
Mitigation: Choose the documented OWS, raw-key, or existing-agent path deliberately and verify the configured wallet, venue, chain, and token requirements before use. <br>


## Reference(s): <br>
- [Simmer Wallet Setup on ClawHub](https://clawhub.ai/simmer/simmer-wallet-setup) <br>
- [Simmer publisher profile](https://clawhub.ai/user/simmer) <br>
- [Open Wallet Standard](https://openwallet.sh) <br>
- [OWS install script](https://docs.openwallet.sh/install.sh) <br>
- [Simmer wallet docs](https://docs.simmer.markets/wallets) <br>
- [Simmer V2 migration guide](https://docs.simmer.markets/v2-migration) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for configuring API keys, wallet selection, local signing, approvals, and troubleshooting.] <br>

## Skill Version(s): <br>
0.3.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
