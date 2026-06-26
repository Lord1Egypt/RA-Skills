## Description: <br>
Helps agents initialize Sentio projects, write and test blockchain processor code, add contracts and ABIs, and deploy processors to the Sentio platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sentioxyz](https://clawhub.ai/user/sentioxyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Sentio blockchain indexers: initialize projects, configure contracts and ABIs, implement multi-chain processors, test handler behavior, and deploy to Sentio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-level analytics and exported event data can expose sensitive user or transaction behavior. <br>
Mitigation: Review wallet addresses, account IDs, transaction identifiers, amounts, rates, points, and webhook exports before production use; prefer aggregated or pseudonymous data where possible. <br>
Risk: Sentio OAuth or API credentials may grant project access beyond the intended processor. <br>
Mitigation: Use scoped credentials for the intended project and keep API keys in secret configuration rather than code or shared examples. <br>


## Reference(s): <br>
- [Advanced Processor Patterns](references/advanced-patterns.md) <br>
- [DeFi Processor Patterns](references/defi-patterns.md) <br>
- [Position Tracking Templates](references/position-tracking-templates.md) <br>
- [Production Processor Examples](references/production-examples.md) <br>
- [Store Entities and Points Systems](references/store-and-points.md) <br>
- [sentioxyz/sentio-processors](https://github.com/sentioxyz/sentio-processors) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline TypeScript, YAML, JSON, GraphQL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may include blockchain addresses and credential placeholders that require review before production use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
