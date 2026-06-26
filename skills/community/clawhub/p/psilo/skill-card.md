## Description: <br>
Use this skill when an agent needs to create on-chain escrow contracts, release escrowed funds through arbiter-signed transactions, and interact with the Pakt Escrow service using the @pakt/psilo SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pakt](https://clawhub.ai/user/pakt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add Pakt escrow workflows to an agent, including escrow creation, status checks, transaction preparation, deposits, release readiness, and final arbiter release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports crypto escrow operations that can create contracts, sign transactions, release funds, and require wallet credentials. <br>
Mitigation: Require manual confirmation for every transaction, use a dedicated low-balance wallet, keep bearer tokens and wallet secrets away from general-purpose agents, and validate on testnets before using real funds. <br>
Risk: The security evidence reports inconsistent transaction examples that require careful review before use with real funds. <br>
Mitigation: Review the SDK and contract behavior against authoritative source code or API documentation, and verify ERC20 funding and updateStatus response handling before production use. <br>


## Reference(s): <br>
- [psilo Skill Page](https://clawhub.ai/pakt/psilo) <br>
- [@pakt/psilo SDK](https://www.npmjs.com/package/@pakt/psilo) <br>
- [SIWA Skill Documentation](https://siwa.id/skill.md) <br>
- [Evalanche](https://www.npmjs.com/package/evalanche) <br>
- [SIWA Protocol Spec](https://siwa.id/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes escrow API usage, wallet/authentication setup, transaction-signing examples, and security checklist guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
