## Description:

Provides end-to-end Bitnow network API workflows for wallet signature authentication, on-chain top-up verification, consumer API key lifecycle management, model gateway calls, and balance or usage queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viyozc](https://clawhub.ai/user/viyozc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate concrete, API-first guidance for Bitnow onboarding, wallet authentication, balance top-ups, API key administration, model calls, and usage troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions involving wallet funds and on-chain deposits.

Mitigation: Use only a verified Bitnow gateway and independently confirm the blockchain network, token address, and contract address before approving or depositing funds.

Risk: The workflows may expose reusable credentials, session tokens, API keys, wallet signatures, or upstream provider secrets in prompts or shared outputs.

Mitigation: Redact tokens, API keys, signatures, and provider credentials before sharing logs or responses, and avoid supplier/provider workflows unless explicitly authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viyozc/skills/spherico-agent)
- [Bitnow gateway test API](https://gateway-test.bitnow.ai)
- [Base Sepolia RPC endpoint](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, request bodies, endpoint placeholders, and troubleshooting steps.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
