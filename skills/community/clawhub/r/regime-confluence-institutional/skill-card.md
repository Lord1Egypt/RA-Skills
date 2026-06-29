## Description: <br>
Institutional-grade regime confluence with full multi-asset context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request a paid APEX Runner regime-confluence signal before large multi-day positions or when multi-asset market context is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each invocation can spend USDC from an EVM wallet on Base mainnet. <br>
Mitigation: Use a dedicated low-balance wallet and configure the agent to ask before making paid calls. <br>
Risk: Exposure of EVM_PRIVATE_KEY can compromise the wallet used for paid requests. <br>
Mitigation: Store the private key only in a secure environment variable or secret manager and keep it out of prompts, logs, and shared files. <br>
Risk: The returned market signal may be incomplete, stale, or unsuitable as the sole basis for a trading decision. <br>
Mitigation: Treat the response as one input to a broader review process and confirm material decisions with independent analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/regime-confluence-institutional) <br>
- [APEX Runner regime confluence institutional signal](https://apexrunner.ai/signals/regime-confluence-institutional) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>
- [Related signal: regime confluence](https://apexrunner.ai/signals/regime-confluence) <br>
- [Related signal: regime transition probability institutional](https://apexrunner.ai/signals/regime-transition-probability-institutional) <br>
- [Related signal: apex alpha score institutional](https://apexrunner.ai/signals/apex-alpha-score-institutional) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, API calls, guidance] <br>
**Output Format:** [Markdown guidance with a Python example and JSON API response.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and an EVM wallet with USDC on Base mainnet for paid x402 calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
