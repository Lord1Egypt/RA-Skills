## Description:

Captures operations process bottlenecks, incident patterns, capacity issues, automation gaps, SLA breaches, and toil accumulation for continuous operations improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operations teams use this skill to capture recurring incidents, SLO/SLA breaches, capacity issues, automation gaps, process bottlenecks, and toil as structured local Markdown records that can be reviewed and promoted into operational standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent operations logs can capture sensitive incident details, secrets, internal infrastructure identifiers, or customer data if entries are written carelessly.

Mitigation: Redact log excerpts, mask hostnames, account IDs, credentials, IP addresses, and PII, and avoid storing customer data in .learnings records.

Risk: Optional hooks persist across sessions and may inspect command output for operational signals.

Mitigation: Enable hooks only when reminders are desired, keep them project-scoped, use narrow matchers, and avoid logging raw command output, secrets, or transcripts.

Risk: Promoting learnings into agent instructions, hooks, memory files, runbooks, or generated skills can change future agent behavior.

Mitigation: Show a reviewed diff and apply promotion changes only after explicit user approval; treat generated skills as untrusted until human-reviewed.

Risk: Cross-skill reading can expose unrelated skill context when stackable mode is used.

Mitigation: Do not let the skill read other skill folders unless cross-linking is explicitly needed, and keep writes scoped to the operations namespace.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hooks Setup](references/hooks-setup.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/skills/self-improving-operations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown entries, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends local .learnings records and may propose reviewed promotions to runbooks, postmortems, automation backlog items, capacity models, handoff checklists, SLO definitions, agent instructions, hooks, or generated skills.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
