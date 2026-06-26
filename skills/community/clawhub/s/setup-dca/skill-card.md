## Description: <br>
Set up a non-custodial dollar-cost averaging strategy on Uniswap for recurring swaps, route selection, USDC approval, automation, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure recurring, non-custodial token purchases on Uniswap with route selection, cost projection, optional first execution, and self-execute or Gelato automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize recurring on-chain trades rather than a single swap. <br>
Mitigation: Confirm the wallet, token pair, per-trade amount, maximum total budget, schedule, end date, and cancellation process before enabling automation. <br>
Risk: Gelato mode may require ongoing keeper funding and can continue executing autonomously. <br>
Mitigation: Review the Gelato funding source, expected keeper fees, and pause or cancellation steps before creating the automation task. <br>
Risk: A misconfigured DCA strategy can spend more than intended over time. <br>
Mitigation: Require explicit user confirmation of the full strategy, total budget, slippage tolerance, and spending limits before any execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/setup-dca) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill specification](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown status summaries with transaction details and optional JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .uniswap/dca-config.json for self-execute mode and may trigger a first on-chain swap after explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
