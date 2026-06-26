## Description: <br>
Seller-side TyrPay workflow for LLM agents. Accept tasks, execute zkTLS-proven API calls, submit proof bundles, and monitor settlement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10000-c](https://clawhub.ai/user/10000-c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to run the seller side of a TyrPay payment flow, including accepting funded tasks, making zkTLS-proven upstream API calls, submitting proof bundles, and monitoring settlement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires private keys and API secrets that can authorize transactions or account actions. <br>
Mitigation: Use scoped, revocable credentials where possible; keep .env files out of source control, chat, and shared storage. <br>
Risk: Seller execution depends on correct settlement chain, wallet, contract, verifier, and task state configuration. <br>
Mitigation: Run readiness checks first and verify chain ID, settlement contract, signer access, verifier signer address, and task funding state before accepting or submitting proofs. <br>
Risk: In-memory storage is not retrievable across buyer, seller, and verifier processes in real multi-party flows. <br>
Mitigation: Use persistent shared storage such as 0G, IPFS, or HTTP for production or cross-agent workflows. <br>


## Reference(s): <br>
- [Tool Reference](references/tool-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/10000-c/tyrpay-seller-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with structured tool-call inputs and status outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wallet private keys, API credentials, configured settlement contract access, storage adapter access, and zkTLS adapter access.] <br>

## Skill Version(s): <br>
0.1.13 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
