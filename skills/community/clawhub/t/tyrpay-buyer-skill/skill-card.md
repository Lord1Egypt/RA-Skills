## Description:

Buyer-side TyrPay workflow for LLM agents. Create tasks, optionally wait for seller commitment, fund tasks explicitly, monitor settlement, and request refunds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10000-c](https://clawhub.ai/user/10000-c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, fund, monitor, and refund buyer-side TyrPay settlement tasks while validating seller commitment expectations before payment is locked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can require raw private keys and wallet-level payment authority.

Mitigation: Use a dedicated low-value wallet, avoid committing .env files, and prefer a hardware wallet, KMS, or secret manager where possible.

Risk: Mutable package installs or untrusted registries can change the runtime behavior of the buyer workflow.

Mitigation: Pin dependency versions and install packages only from trusted registries.

Risk: Funds can be locked under unintended seller commitment terms if buyer expectations are omitted or wrong.

Mitigation: Require and review expectations on every funding path before calling tyrpay_post_task without createOnly or tyrpay_fund_task.

Risk: Untrusted storage adapters, RPC endpoints, or verifier services can affect task monitoring and settlement decisions.

Mitigation: Use trusted storage adapters, RPC providers, and verifier endpoints, and review task status before settlement or refund actions.

## Reference(s):

- [Tool Reference](references/tool-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Tool calls]

**Output Format:** [Markdown guidance with inline tool names, configuration variables, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce buyer workflow tool-call sequences and status interpretation.]

## Skill Version(s):

0.1.8 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
