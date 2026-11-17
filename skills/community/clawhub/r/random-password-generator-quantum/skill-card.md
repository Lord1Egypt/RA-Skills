## Description:

Generates high-entropy passwords with configurable length, character classes, ambiguity filtering, and quantum or standard randomness through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and credential-management workflows use this skill to request configurable passwords for onboarding, rotation, system accounts, authentication, and other security-sensitive setup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords for high-value systems may be visible to the third-party remote service.

Mitigation: Use this skill only when policy allows AgentPMT to process the generated credential; prefer local generation for secrets that must be known only to the requester.

Risk: Remote setup details, schemas, or endpoints may change after installation.

Mitigation: Refresh or reinstall the skill before production use and fetch live schema details when parameters or response fields are unclear.

## Reference(s):

- [Random Password Generator Quantum schema](artifact/schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/random-password-generator-quantum)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/random-password-generator-quantum)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool responses include the generated password, character count, randomness source, and enabled character types.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
