## Description: <br>
Signet helps agents check spotlight ad prices, list current ads or signatures, and post URLs to Signet onchain advertising on Hunt Town using x402 payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebayaki](https://clawhub.ai/user/sebayaki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to estimate Signet spotlight costs, inspect current advertising activity, and prepare URL placement through the x402 payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend crypto and publish spotlight ads. <br>
Mitigation: Run simulation or estimate first, then require explicit approval for the exact URL, duration, wallet, network, and cost before any real post. <br>
Risk: Posting can involve a raw wallet private key and an npm CLI. <br>
Mitigation: Use a dedicated low-balance wallet, avoid passing valuable private keys on the command line, and pin and verify the npm CLI before use. <br>


## Reference(s): <br>
- [ClawHub Signet release](https://clawhub.ai/sebayaki/signet) <br>
- [Signet service](https://signet.sebayaki.com) <br>
- [Signet x402 estimate API](https://signet.sebayaki.com/api/x402/estimate?guaranteeHours=0) <br>
- [Signet signature list API](https://signet.sebayaki.com/api/signature/list?startIndex=0&endIndex=5) <br>
- [Signet x402 spotlight API](https://signet.sebayaki.com/api/x402/spotlight) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cost-estimation, listing, simulation, or posting commands; real posting requires explicit approval of URL, duration, wallet, network, and cost.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
