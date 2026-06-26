## Description: <br>
Feedback forensics for ERC-8004 agents. Detects Sybil rings, fake reviews, rating manipulation, and reputation laundering across 20 chains. No API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goatgaucho](https://clawhub.ai/user/goatgaucho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check ERC-8004 agent reputation before payment, escrow, hiring, or delegation. It guides agents through TrustLayer API lookups for Sybil risk, fake reviews, rating manipulation, cross-chain reputation laundering, and exposure limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TrustLayer API lookups can expose queried agent IDs, wallet addresses, IP/timing metadata, and lookup patterns to a third-party service. <br>
Mitigation: Get user approval before sensitive due-diligence lookups and avoid sending private or unnecessary identifiers. <br>
Risk: Some endpoints may cost money through x402 micropayments or return payment requirements after free rate limits. <br>
Mitigation: Require explicit approval before paid endpoints, repeated leaderboard calls after free limits, or workflows that could trigger charges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goatgaucho/trustlayer-sybil-scanner) <br>
- [TrustLayer homepage](https://thetrustlayer.xyz) <br>
- [TrustLayer API base](https://api.thetrustlayer.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, text, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; some TrustLayer endpoints may require x402 micropayments or be rate-limited.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
