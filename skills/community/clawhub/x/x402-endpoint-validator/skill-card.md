## Description:

Validate x402 endpoints by testing 402 responses, Bazaar extension support, payment schemas, and .well-known/x402 discovery manifests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marketingkioldenburg](https://clawhub.ai/user/marketingkioldenburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to check whether x402-protected services return the expected payment challenge, advertise Bazaar metadata, and expose a valid discovery manifest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation commands make HTTP requests to endpoints selected by the user.

Mitigation: Use only intended test endpoints and avoid secrets, private customer data, or production-only payloads unless that exposure is deliberate.

## Reference(s):

- [x402 Homepage](https://www.x402.org)
- [Agentic Market Validator](https://agentic.market/validate)
- [ClawHub Skill Page](https://clawhub.ai/marketingkioldenburg/skills/x402-endpoint-validator)
- [Publisher Profile](https://clawhub.ai/user/marketingkioldenburg)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline bash code blocks and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for endpoint checks; examples make HTTP requests to user-selected endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
