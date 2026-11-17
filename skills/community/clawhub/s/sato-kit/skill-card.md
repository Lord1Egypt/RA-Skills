## Description:

Guides agents through onchain reads, swap quotes, swaps, and x402 payments using Sato Kit's policy pre-flight, simulation, approval, and receipt workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satohubai](https://clawhub.ai/user/satohubai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read EVM chain state, quote swaps, and prepare swaps or x402 payments for human review before submitting an approved intent to a signer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An external npm CLI can prepare or execute financial actions.

Mitigation: Review the policy file, keep the default fork mode unless intentionally opting into mainnet, and inspect the summary, fees, simulation, and policy result before approving the exact intent ID.

Risk: Local intent-related data could be disclosed if committed to version control.

Mitigation: Keep .sato out of version control.

## Reference(s):

- [Sato Kit homepage](https://satohub.ai)
- [Sato Kit on ClawHub](https://clawhub.ai/satohubai/skills/sato-kit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands; CLI responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preparation returns an intent for review; execution requires approval of its exact intent ID.]

## Skill Version(s):

0.1.1 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
