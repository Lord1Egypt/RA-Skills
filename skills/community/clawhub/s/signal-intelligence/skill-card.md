## Description: <br>
Aggregated signal quality score across all active APEX modules <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request a paid, real-time APEX signal quality score before committing capital or calibrating confidence across active trading signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to make paid x402 calls, so each use can spend wallet funds. <br>
Mitigation: Use a dedicated low-balance wallet, verify the endpoint and cost before execution, and avoid primary or broad-purpose private keys. <br>


## Reference(s): <br>
- [Signal Intelligence endpoint](https://apexrunner.ai/signals/signal-intelligence) <br>
- [Signal pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner](https://apexrunner.ai) <br>
- [ClawHub listing](https://clawhub.ai/kynto2001-ctrl/skills/signal-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [json, code, guidance] <br>
**Output Format:** [JSON responses with Markdown usage guidance and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and may spend wallet funds for x402 paid calls on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
