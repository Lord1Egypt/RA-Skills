## Description: <br>
Real-time institutional transaction monitoring for asset tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request whale-flow signals for a supplied asset ticker and return the resulting market-monitoring response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker requests are sent to an external whale-flow API. <br>
Mitigation: Use the skill only when sharing the requested ticker with the external service is acceptable. <br>
Risk: Premium results may ask the user to send SOL to a listed wallet or use a pricing page. <br>
Mitigation: Pay only after independently verifying the publisher, service, and payment destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/whale-scanner) <br>
- [Premium pricing page](https://ssyopros.zo.space/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response or payment-required message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depends on the requested ticker and may include premium-payment information returned by the external service.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
