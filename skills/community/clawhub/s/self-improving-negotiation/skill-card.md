## Description:

Logs redacted negotiation learnings, issues, and feature requests for concession leaks, BATNA gaps, framing misses, objections, agreement risk, and optional project-scoped reminder hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and negotiation teams use this skill to capture redacted negotiation patterns, risks, and tooling requests in local markdown files. It helps agents propose reviewed improvements such as playbooks, objection libraries, concession guardrails, BATNA checklists, and deal review templates without accepting terms or approving deals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive negotiation details such as BATNA values, pricing floors, confidential terms, legal advice, approval tokens, or raw transcripts could be captured in local learning files.

Mitigation: Log only redacted process-level summaries, keep .learnings private or access-controlled, and review entries before committing or sharing them.

Risk: Reminder hooks could create excessive or overly broad negotiation prompts if installed globally or configured with broad matchers.

Mitigation: Use project-scoped hooks only, avoid empty or catch-all matchers, and keep hook behavior reminder-only.

Risk: Generated skill scaffolds could introduce weak or misleading negotiation guidance if published without review.

Mitigation: Keep extraction dry-run by default, pass --write only after explicit user approval, and review any generated SKILL.md before enabling or publishing it.

Risk: Negotiation suggestions could be mistaken for authority to accept terms, set pricing, approve concessions, or finalize agreements.

Mitigation: Require explicit human approval for high-impact concessions and final terms; the skill must remain logging and reminder focused.

## Reference(s):

- [Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning-log entries, reminder text, and optional reviewed skill scaffold guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
