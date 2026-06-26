## Description: <br>
Zhentan is an onchain security agent and co-signer that monitors pending multisig transactions, screens them against behavioral and security risk signals, and helps approve, reject, analyze, or queue transactions and invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koshikraj](https://clawhub.ai/user/koshikraj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Safe owners and operators use Zhentan to review pending multisig transactions, inspect risk scores, approve or reject transactions, manage screening rules, and queue invoices through a conversational agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give chat-driven authority to execute on-chain transactions and change security controls through the Zhentan service. <br>
Mitigation: Install only after verifying server-side authorization, transaction previews, audit logs, secret revocation, and safeguards for disabling screening or changing rules. <br>
Risk: API calls rely on AGENT_SECRET, and misuse or exposure of that token could allow unauthorized actions. <br>
Mitigation: Protect the secret, scope access conservatively, rotate or revoke it if exposed, and begin with low-value assets or limited permissions before granting access to important wallets. <br>


## Reference(s): <br>
- [ClawHub Zhentan skill page](https://clawhub.ai/koshikraj/zhentan) <br>
- [Zhentan API base URL](https://api.zhentan.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an AGENT_SECRET bearer token; reports API results such as transaction status, risk findings, and invoice state.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
