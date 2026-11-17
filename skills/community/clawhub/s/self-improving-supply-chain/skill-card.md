## Description:

Captures supply chain learnings, disruptions, and feature requests in Markdown so agents can document forecast errors, supplier risks, logistics delays, inventory mismatches, quality deviations, and demand signal shifts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Supply chain operators, planners, procurement teams, logistics teams, quality teams, and supporting developers use this skill to record operational issues and reusable improvement patterns. It helps agents create structured Markdown entries and propose reviewed promotions to supplier scorecards, safety stock policies, routing playbooks, demand planning models, quality criteria, or related agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning logs could include confidential supplier pricing, contract terms, or customer-identifiable order data.

Mitigation: Record aggregated metrics and redacted summaries, and avoid raw purchase order numbers, customer names, negotiated pricing, or contract terms.

Risk: Optional hooks can inject reminders, and the PostToolUse detector can inspect command output when enabled.

Mitigation: Keep hooks project-scoped, enable only the reminder hook by default, and use the PostToolUse detector only when command-output inspection is acceptable.

Risk: Promoting learnings into agent guidance, hooks, memory files, or generated skills can change future agent behavior.

Mitigation: Show a reviewed diff and apply promotions only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jose-compu/skills/self-improving-supply-chain)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash snippets, JSON hook examples, and JavaScript/TypeScript hook code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends local learning logs and can emit optional reminder text through project-scoped hooks; it does not execute procurement or payment actions.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
