## Description: <br>
Manage LUKSO Universal Profiles - identity, permissions, tokens, blockchain operations, with cross-chain support for Base and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frozeman](https://clawhub.ai/user/frozeman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage LUKSO Universal Profiles, controller permissions, profile metadata, token operations, gasless LUKSO relay flows, and cross-chain deployment data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local controller keys to submit irreversible blockchain transactions. <br>
Mitigation: Manually inspect every direct, relay, batch, transfer, mint, and permission-changing transaction before allowing an agent to run it; test on testnet first. <br>
Risk: A funded or highly privileged Universal Profile could be exposed to excessive controller permissions. <br>
Mitigation: Use a least-privilege controller, avoid full-access permissions, and prefer restricted permissions such as CALL over SUPER_CALL where possible. <br>
Risk: Controller private keys may be stored locally for signing. <br>
Mitigation: Keep key files locked down, use restrictive file permissions, and avoid logging, printing, or transmitting private keys. <br>


## Reference(s): <br>
- [ERC725.js Complete Reference](references/ERC725-JS.md) <br>
- [LUKSO Docs](https://docs.lukso.tech/) <br>
- [LSP6 Key Manager](https://docs.lukso.tech/standards/access-control/lsp6-key-manager) <br>
- [ERC725.js](https://github.com/ERC725Alliance/erc725.js) <br>
- [Universal Everything](https://universaleverything.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell, JavaScript, JSON, and transaction examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain transaction, relay, permission, and credential-handling guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.9.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
