## Description:

Paid microservices for AI agents, served over x402 v2 (USDC on Base).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiyesum](https://clawhub.ai/user/hiyesum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to access paid x402 services for crypto snapshots, utilities, research, extraction, grading, monitoring, payment verification, and related endpoint tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls can authorize USDC payments on Base.

Mitigation: Check the amount and recipient before signing, and use a wallet with limited funds.

Risk: Submitted content goes to the external provider, and memory or webhook content may be retained for a limited time; privacy and access-control claims were not independently verified.

Mitigation: Choose carefully what to submit, especially what you place in the memory store or webhook inbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hiyesum/skills/yesum-agent-services)
- [Source repository (server-resolved provenance)](https://github.com/hiyesum/yesum-clawhub-skill)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Python and JavaScript code]

**Output Format:** [JSON service responses; some responses contain extracted Markdown or generated Python/JavaScript code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by endpoint and may include identifiers for time-limited monitoring, inbox, schedule, or memory services.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
