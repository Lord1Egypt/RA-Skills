## Description:

Create a recoverable active-work brief for context-heavy coding, design, debugging, review, research, or handoff sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture recoverable active-work state for coding, design, debugging, review, research, and handoff sessions. It emphasizes evidence-first scanning, source tags, confidence labels, verification state, and concrete next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated briefs may include repository state, git diffs, command history, user decisions, session-visible context, secrets, customer data, or private plans.

Mitigation: Review generated briefs before sharing them outside the project and remove sensitive content.

Risk: The skill can preserve unverified or incomplete state if available evidence is missing or uncertain.

Mitigation: Use the required source tags, confidence labels, unknowns, and verification-state fields to distinguish established evidence from unresolved context.

## Reference(s):

- [Compact Brief Scaffold](references/compact-brief.md)
- [ClawHub Skill Page](https://clawhub.ai/kkenny0/skills/taku-compact)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown brief with structured YAML fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the latest and timestamped briefs under .taku/context/ when the host permits file writes; otherwise returns the brief in chat.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
