## Description:

Build, review, or test KYA (Know Your Agent) human-gate controls for AI agents that prepare or execute regulated financial actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance reviewers, and risk teams use this skill to design, review, or test human-gate controls for regulated financial agent actions such as payments, withdrawals, stablecoin off-ramps, lending, onboarding, and account-control changes. It helps agents produce action-bound approval plans, delegation receipt checks, audit evidence plans, and evaluation cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python receipt issuer can sign financial authorization receipts from unverified approval evidence.

Mitigation: Use the receipt issuer only as a design and testing aid unless evidence verification, approver independence, caller authentication, and strict permission boundaries are implemented outside the agent.

Risk: A self-contained HMAC receipt guard is not a production-grade authorization boundary for regulated financial actions.

Mitigation: Place production signing in a managed KMS or HSM, rotate keys by key ID, verify receipts at the executor, and combine nonce consumption with an idempotent execution record.

Risk: Human-gate guidance may be mistaken for regulatory certification or legal advice.

Mitigation: State which controls are implemented, mocked, provider-backed, or still require legal and compliance approval before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carochen112233-commits/skills/regulated-agent-human-gate)
- [Human Gate Policy](artifact/resources/human-gate-policy.md)
- [Identity Verification Routing](artifact/resources/identity-verification-routing.md)
- [Audit Evidence Checklist](artifact/resources/audit-evidence-checklist.md)
- [Agent Evaluation Guide](artifact/resources/agent-evaluation-guide.md)
- [Risk Taxonomy](artifact/resources/risk-taxonomy.md)
- [Regulated Finance Use Cases](artifact/resources/regulated-finance-use-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and YAML templates, Python command examples, and structured control checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces action-intent, gate-decision, audit, MCP contract, policy, receipt, and evaluation artifacts for agent workflows.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
