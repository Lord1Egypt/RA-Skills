## Description:

Technical Lead skill for first-line acceptance, progress tracking, risk escalation, and evidence review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to perform first-line acceptance of specialist work, track progress, review evidence quality, and prepare concise handoffs for final technical review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be triggered by general review terms in environments with multiple review-oriented skills.

Mitigation: Invoke it explicitly for first-line acceptance and progress tracking when routing ambiguity could affect the review workflow.

Risk: Acceptance decisions can be misleading when specialist claims are not backed by concrete test, runtime, documentation, or diff evidence.

Mitigation: Require real evidence for accepted work, return incomplete items with precise correction criteria, and record unresolved risks before handoff.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with acceptance decisions, progress summaries, missing-evidence lists, risk notes, and handoff notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or hidden persistence; outputs should preserve specialist evidence and distinguish accepted, partial, returned, and blocked work.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
