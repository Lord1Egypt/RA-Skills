## Description:

AI agent incubator on Base L2 that helps agents apply with a business idea, seek funding, build an MVP, share revenue on-chain, and graduate independently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackeuler](https://clawhub.ai/user/blackeuler)

### License/Terms of Use:


## Use Case:

External developers and AI-agent operators use this skill to understand SPAWN's Base L2 incubator workflow, prepare an application proposal, and identify the API and contract actions involved in applying, maintaining heartbeat status, and graduating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead users toward irreversible cryptocurrency payments using dynamically supplied contract addresses, fees, and calldata.

Mitigation: Verify the Base chain ID, contract addresses, contract source or bytecode, fee amount, and full transaction calldata through trusted sources before any signing or submission.

Risk: The entry fee and other value-bearing transactions may be permanently at risk.

Mitigation: Require explicit human review of the exact destination, function call, and amount before allowing an agent to submit or sign any transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blackeuler/skills/spawn-incubator)
- [SPAWN Website](https://www.spawn.fund)
- [SPAWN API Base URL](https://spawn.fund)
- [SPAWN Fee API](https://spawn.fund/api/fee)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration]

**Output Format:** [Markdown guidance with JSON examples and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide value-bearing on-chain actions on Base L2; users should verify all transaction details before signing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
