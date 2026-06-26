## Description: <br>
Provides API reference guidance for querying Compass TSS cross-chain transaction status, scanned block heights, pending transactions, orders, and transaction hashes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbtsm](https://clawhub.ai/user/lbtsm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support operators use this skill to ask an agent for endpoint, parameter, response, and curl guidance when checking cross-chain transaction records through the Compass TSS API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction hashes, order IDs, chain IDs, or block heights used in queries may be sent to tss-api.chainservice.io. <br>
Mitigation: Avoid submitting identifiers that should not be shared with that provider, and review requests before using the external service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbtsm/tss-api) <br>
- [Compass TSS API base URL](https://tss-api.chainservice.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown API guidance with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API reference; examples may include chain IDs, block heights, order IDs, and transaction hashes.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
