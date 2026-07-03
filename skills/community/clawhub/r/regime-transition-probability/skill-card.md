## Description: <br>
Probabilistic regime transition forecast with timing estimate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and trading teams use this skill to request a paid, real-time regime transition probability and timing estimate for dynamic strategy allocation and regime-aware hedging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a live EVM private key that an agent can use while making requests. <br>
Mitigation: Use only a dedicated low-balance wallet for this skill and never expose a main wallet private key. <br>
Risk: Agent calls can trigger paid Base USDC requests, and repeated calls may spend funds unexpectedly. <br>
Mitigation: Confirm the current call cost before use and rely on external wallet controls, low balances, or manual approval for spending limits. <br>
Risk: The response is a probabilistic trading signal and may be incorrect or unsuitable for a specific strategy. <br>
Mitigation: Treat the signal as decision support, validate it against independent risk controls, and avoid automated trading solely from this output. <br>


## Reference(s): <br>
- [APEX Runner regime transition probability signal](https://apexrunner.ai/signals/regime-transition-probability) <br>
- [APEX Runner pricing tier lookup](https://apexrunner.ai/signals/my-pricing) <br>
- [Related signal: regime transition](https://apexrunner.ai/signals/regime-transition) <br>
- [Related signal: regime confluence](https://apexrunner.ai/signals/regime-confluence) <br>
- [Related signal: regime transition probability institutional](https://apexrunner.ai/signals/regime-transition-probability-institutional) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Guidance] <br>
**Output Format:** [Markdown usage guidance with Python example code and a JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and a Base mainnet USDC wallet payment for each call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
