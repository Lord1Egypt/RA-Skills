## Description: <br>
x402 Compute helps agents provision and manage paid GPU/VPS instances, use decentralized OpenAI-compatible grid inference, and operate TEE-backed compute nodes through wallet/API-key authenticated workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivaavimusic](https://clawhub.ai/user/ivaavimusic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external agent users use this skill to browse compute plans, provision and manage paid cloud instances, call grid inference endpoints, and follow node-operator workflows for providing compute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage paid compute and wallet-backed signing flows. <br>
Mitigation: Use a dedicated low-balance wallet, set spending limits, and review paid actions before execution. <br>
Risk: Private keys, Solana signer keys, and compute API keys are sensitive credentials. <br>
Mitigation: Store credentials securely, avoid primary custody wallets, and rotate or delete credentials that may have been exposed. <br>
Risk: Password fallback files and one-time root passwords can expose instance access. <br>
Mitigation: Prefer SSH keys, protect any saved .compute_password_* file, and delete password material when it is no longer needed. <br>
Risk: OWS and node-operation flows may invoke external tooling or installers. <br>
Mitigation: Install OWS from a pinned trusted source and inspect the node installer before running background services. <br>


## Reference(s): <br>
- [x402 Compute documentation](https://docs.x402layer.cc/agentic-access/x402-compute) <br>
- [x402 Compute cloud console](https://cloud.x402compute.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ivaavimusic/x402-compute) <br>
- [API reference](references/api-reference.md) <br>
- [Node operator guide](references/node-operator.md) <br>
- [OpenWallet / OWS guide](references/openwallet-ows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that create, resize, extend, destroy, or inspect paid compute resources and grid inference access.] <br>

## Skill Version(s): <br>
1.8.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
