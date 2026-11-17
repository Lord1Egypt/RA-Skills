## Description:

Structured web research and synthesis for investigating topics, comparing options, gathering sources, and producing research briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through scoped web research, source extraction, comparison, and concise research brief writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to engage for general research-like phrasing.

Mitigation: Confirm scope, constraints, and assumptions before conducting searches or producing a brief.

Risk: The optional shell helper uses a topic-derived temporary directory path.

Mitigation: Avoid running the helper with untrusted topic strings unless its temporary directory handling is hardened.

## Reference(s):

- [Advanced Research Patterns](references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research brief with citations, source lists, optional comparison tables, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires factual claims to be cited and asks the agent to flag contradictory, stale, or unsourced findings.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
