## Description: <br>
ProxyGate CLI routes ProxyGate-related user requests to setup, status, buying, selling, jobs, or update sub-skills for marketplace workflows involving proxy requests, USDC payments, Solana wallets, listings, tunnels, and jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this router skill to choose the right ProxyGate sub-skill for setup, account status, API buying, API selling, bounty jobs, and CLI or SDK updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routed workflows can involve deposits, withdrawals, wallet signing, listing changes, job submissions, proxy requests, and tunnels. <br>
Mitigation: Require explicit approval before those actions and review the selected ProxyGate sub-skill before use. <br>
Risk: Proxy calls may transmit secrets or sensitive payloads through a gateway and selected listing. <br>
Mitigation: Avoid sending secrets through ProxyGate proxy calls unless the user trusts the gateway and the selected listing. <br>


## Reference(s): <br>
- [ProxyGate Gateway](https://gateway.proxygate.ai) <br>
- [ProxyGate Docs](https://gateway.proxygate.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests to ProxyGate sub-skills; no executable code is included in this router artifact.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
