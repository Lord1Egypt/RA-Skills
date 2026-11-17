## Description:

Track and cap x402 spend across providers with per-endpoint hard and soft caps, pre-authorized override budgets, cumulative spend tracking, and monthly ceilings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marketingkioldenburg](https://clawhub.ai/user/marketingkioldenburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep x402 pay-per-request API usage within configured budgets before an agent pays for a request. It provides policy guidance for endpoint caps, pre-authorized overrides, cumulative spend tracking, and audit logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured budgets may still allow payments that are within the approved cap.

Mitigation: Review hard caps, soft caps, override budgets, monthly ceilings, and session ceilings before connecting the policy to an x402 client.

Risk: Spend logs can contain payment metadata.

Mitigation: Keep spend-log.json private and restrict access to audit or operational personnel who need it.

Risk: An agent could exceed intended spend if it can raise its own ceiling during a run.

Mitigation: Use pre-authorized override budgets and require operator approval for future ceiling changes instead of runtime self-approval.

## Reference(s):

- [x402 protocol homepage](https://www.x402.org)
- [ClawHub skill page](https://clawhub.ai/marketingkioldenburg/skills/x402-budget-manager)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces budget policy guidance and examples; it does not bundle executable code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
