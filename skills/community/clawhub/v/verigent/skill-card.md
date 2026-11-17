## Description:

Verify the reputation of any AI agent or skill before transacting, including chain-of-custody provenance for skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extropyconsulting](https://clawhub.ai/user/extropyconsulting)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Verigent to check counterparty reputation, inspect skill provenance, and decide whether to proceed before transactions, sensitive data sharing, or high-stakes agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a remote reputation service for sensitive trust and payment-adjacent decisions.

Mitigation: Treat trust scores as advice and require user review before making payments, sharing sensitive data, or refusing a user-requested action.

Risk: The security evidence flags an unpinned MCP package for a workflow that handles financial and agent-trust decisions.

Mitigation: Install a pinned, audited server version and run it in a constrained environment with only the required environment variables.

Risk: Agent identifiers, payment proofs, and transaction metadata may be sent to Verigent.

Mitigation: Send only the data required for the check and review the service privacy terms before use.

## Reference(s):

- [Verigent homepage](https://verigent.link)
- [ClawHub skill page](https://clawhub.ai/extropyconsulting/skills/verigent)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with HTTP and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include agent identifiers, payment proofs, transaction metadata, trust scores, recommendations, and provenance summaries.]

## Skill Version(s):

0.1.2 (source: server release metadata, created 2026-03-03T22:40:29Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
