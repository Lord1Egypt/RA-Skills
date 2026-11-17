## Description:

Seller-side TyrPay workflow for LLM agents. Accept tasks, execute zkTLS-proven API calls, submit proof bundles, and monitor settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10000-c](https://clawhub.ai/user/10000-c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run the seller side of a TyrPay task: accepting buyer tasks, executing zkTLS-proven API calls, submitting proof bundles, and monitoring settlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys, storage private keys, Reclaim secrets, and model API keys are high-value secrets used by the seller workflow.

Mitigation: Keep secrets out of version control and logs, and run the workflow only in an environment intended to sign TyrPay settlement transactions.

Risk: Unpinned or unexpected package names could change the behavior of a payment-signing runtime.

Mitigation: Use trusted package names and pinned versions where possible before installing the TyrPay seller packages and optional zkTLS dependencies.

Risk: Local memory storage is not retrievable across buyer and verifier processes in real multi-party flows.

Mitigation: Use persistent shared storage such as 0G, IPFS, or HTTP for production or cross-agent workflows.

Risk: Incorrect settlement ABI, verifier signer, endpoint, or model commitment data can cause invalid settlement state or proof submission.

Mitigation: Verify the current settlement ABI, use the registry-authorized verifier signer, and commit only to the endpoint and model resolved by the 0G TeeTLS adapter metadata.

## Reference(s):

- [Tool Reference](references/tool-reference.md)
- [Tyrpay Seller Skill on ClawHub](https://clawhub.ai/10000-c/skills/tyrpay-seller-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tool names, workflow steps, and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes seller status names, environment variables, and operational constraints for TyrPay settlement workflows.]

## Skill Version(s):

0.1.13 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
