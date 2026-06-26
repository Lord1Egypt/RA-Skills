## Description: <br>
Buyer-side TyrPay workflow for LLM agents. Create tasks, optionally wait for seller commitment, fund tasks explicitly, monitor settlement, and request refunds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10000-c](https://clawhub.ai/user/10000-c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent acts as a buyer in a TyrPay payment flow, including creating tasks, validating seller commitments, funding tasks, checking status, and requesting refunds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent wallet-based payment authority without clear spending caps or human approval gates. <br>
Mitigation: Use a dedicated low-balance wallet and require human confirmation with per-transaction and total spending limits before any funding action. <br>
Risk: The skill depends on external packages, a settlement contract, and a target chain for payment execution. <br>
Mitigation: Pin and verify external packages, then check the settlement contract address and chain configuration before use. <br>
Risk: The workflow requires sensitive wallet credentials. <br>
Mitigation: Store buyer and storage private keys securely and avoid reusing high-value wallets for agent-managed payments. <br>


## Reference(s): <br>
- [Tool Reference](references/tool-reference.md) <br>
- [ClawHub Release Page](https://clawhub.ai/10000-c/tyrpay-buyer-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool names, workflow steps, configuration variables, and status descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of buyer-side TyrPay tools that return structured task, funding, refund, timeout, and status results.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
