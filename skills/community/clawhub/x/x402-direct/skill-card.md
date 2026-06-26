## Description: <br>
Discover and search x402-enabled services via the x402.direct directory API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JovannyEspinal](https://clawhub.ai/user/JovannyEspinal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent builders use this skill to browse, search, and inspect x402-enabled API services, including service pricing, trust scores, payment details, and ecosystem statistics. It is useful when an agent needs to find crypto-payable services by category, network, score, or natural-language query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid search requests can spend real USDC through x402 payment flow. <br>
Mitigation: Prefer free browse, detail, and stats endpoints when sufficient; require user confirmation or a tightly limited wallet before paid `/api/search` calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JovannyEspinal/x402-direct) <br>
- [x402.direct directory](https://x402.direct) <br>
- [Repository listed in metadata](https://github.com/jovannyespinal/x402-direct-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with API endpoint descriptions, JSON response examples, shell commands, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search can require an x402 payment proof; browse, service details, and stats endpoints are documented as free.] <br>

## Skill Version(s): <br>
1.0.0 (source: metadata.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
