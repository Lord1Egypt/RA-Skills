## Description: <br>
Current market regime label at minimal cost for fast agent loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to fetch a low-cost, real-time crypto market regime label for frequent agent loops, pre-filtering, and deciding when to skip more expensive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can use EVM_PRIVATE_KEY to authorize paid x402 requests for each call. <br>
Mitigation: Use a dedicated low-balance Base wallet funded only with the USDC budget you are willing to spend. <br>
Risk: Frequent agent loops can accumulate per-call costs. <br>
Mitigation: Set loop-level budgets, rate limits, or approval gates before enabling repeated calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/regime-micro) <br>
- [Regime Micro signal endpoint](https://apexrunner.ai/signals/regime-micro) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python example code and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM wallet private key in EVM_PRIVATE_KEY for paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
