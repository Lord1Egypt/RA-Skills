## Description: <br>
Deploy x402 pay-per-call API endpoints in minutes, turning an OpenClaw skill or service into a monetized endpoint accepting USDC on Base with payment verification, pricing, and Cloudflare Tunnel integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyclanker](https://clawhub.ai/user/jimmyclanker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold paid API endpoints that accept USDC on Base, verify payment transactions, and expose the resulting service through local or tunneled deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated endpoints can become publicly reachable when exposed through Cloudflare Tunnel or registered with Spraay. <br>
Mitigation: Review the generated server, add rate limits and input validation, and only publish the tunnel or gateway registration when the endpoint and metadata are intended to be public. <br>
Risk: Payment setup depends on the configured recipient wallet and on-chain verification behavior. <br>
Mitigation: Use only a public recipient wallet address and verify the generated payment logic before relying on the endpoint for paid access. <br>


## Reference(s): <br>
- [x402 Quickstart skill page](https://clawhub.ai/jimmyclanker/x402-quickstart) <br>
- [Spraay Gateway](https://gateway.spraay.app) <br>
- [Base public RPC endpoint](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and generated Node.js/Express project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scaffold creates package.json, .env, .gitignore, and server.js files for a pay-per-call endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
