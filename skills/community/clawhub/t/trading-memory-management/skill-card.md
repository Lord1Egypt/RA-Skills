## Description:

Manages trading decision memory by standardizing logs, extracting lessons, and supporting historical decision retrieval and comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuzimaki](https://clawhub.ai/user/wuzimaki)

### License/Terms of Use:


## Use Case:

External users and trading-system operators use this skill to keep consistent local records of trading decisions, state snapshots, rules, mistakes, and maintenance routines. It supports retrieval and comparison of past decisions inside a PAI trading workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local trading-memory files may contain sensitive strategy, decision rationale, or audit records.

Mitigation: Keep memory paths under user-controlled storage and confirm before archiving or cleaning records needed for audit or review.

Risk: The skill organizes trading decision records but does not validate trading strategy quality or financial suitability.

Mitigation: Treat retrieved lessons and summaries as record-management support, not financial advice or an execution signal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuzimaki/skills/trading-memory-management)
- [Publisher profile](https://clawhub.ai/user/wuzimaki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown and structured local file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for local trading-memory records; it does not bundle executable code.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
