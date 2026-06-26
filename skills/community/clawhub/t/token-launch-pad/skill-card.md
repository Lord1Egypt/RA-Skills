## Description: <br>
Launch tokens with guidance for Clanker, Flaunch, Pump.fun, and the Tator API, including fee economics, claims, recipient updates, and tax and legal awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azep-ninja](https://clawhub.ai/user/azep-ninja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External builders and developers use this skill to evaluate token launch concepts, compare launch platforms, and generate implementation guidance for launching tokens, configuring creator fee recipients, claiming fees, and managing post-launch operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill concerns crypto token launches, fee management, wallet signatures, and irreversible on-chain actions with real financial consequences. <br>
Mitigation: Use a dedicated wallet with minimal funds, verify contract addresses, payment details, fee recipients, and bot-wallet setup before signing or submitting any transaction. <br>
Risk: External API calls and x402 payment signatures can trigger paid requests or launch-related operations. <br>
Mitigation: Confirm the operation, cost, wallet address, token details, and recipient settings before creating or sending a PAYMENT-SIGNATURE or API request. <br>
Risk: The artifact includes reference code patterns for developer infrastructure rather than code executed by the skill itself. <br>
Mitigation: Review, test, and secure any implementation separately, including private-key handling, SDK dependencies, RPC endpoints, and production secrets management. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/azep-ninja/token-launch-pad) <br>
- [Direct Mode Reference](REFERENCE.md) <br>
- [Clanker v4 Direct Mode Reference](references/clanker.md) <br>
- [Flaunch Direct Mode Reference](references/flaunch.md) <br>
- [Pump.fun Direct Mode Reference](references/pumpfun.md) <br>
- [Tator documentation](https://docs.tator.bot) <br>
- [x402 protocol](https://www.x402.org) <br>
- [Clanker SDK documentation](https://clanker.gitbook.io/clanker-documentation/sdk/v4.0.0) <br>
- [Flaunch builder documentation](https://docs.flaunch.gg/for-builders) <br>
- [Pump.fun public documentation](https://github.com/pump-fun/pump-public-docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with code blocks, API examples, command snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may describe external API calls, wallet signatures, unsigned transactions, and blockchain operations.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
