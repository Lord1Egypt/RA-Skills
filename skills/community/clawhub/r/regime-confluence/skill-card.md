## Description: <br>
Multi-timeframe regime agreement score for higher-confidence entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to request a paid real-time crypto regime confluence signal before high-conviction trading entries or when timeframe disagreement increases risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use a wallet private key for automatic paid signal calls. <br>
Mitigation: Use only a dedicated wallet with minimal USDC and never provide a primary wallet private key. <br>
Risk: Automatic x402 payments can spend funds without clear per-call consent boundaries. <br>
Mitigation: Require explicit approval or enforce a strict spending limit for each paid signal call. <br>
Risk: The signal may be mistaken for financial advice. <br>
Mitigation: Treat outputs as trading information only and review them before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/regime-confluence) <br>
- [Regime Confluence signal homepage](https://apexrunner.ai/signals/regime-confluence) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response containing a confluence score, aligned timeframe count, and dominant regime.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment; paid per call using USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
