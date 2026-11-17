## Description:

Structured retrospectives and execution-memory hygiene for OpenClaw agents that capture reusable lessons without hidden memory or autonomous behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebclawops](https://clawhub.ai/user/sebclawops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run post-task retrospectives, log reusable corrections, and review recurring execution patterns while keeping factual memory and execution lessons separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Visible retrospective notes could capture secrets, credentials, or sensitive personal details if the user logs them.

Mitigation: Avoid logging secrets or sensitive personal details, and keep notes in the visible workspace path described by the skill.

Risk: A proposed global lesson could influence future agent behavior incorrectly if promoted from weak evidence.

Mitigation: Use the observed, repeated, candidate rule, and confirmed rule states, and review proposed global promotions before relying on them.

Risk: Retrospective notes could become a duplicate factual memory system if used for events, dates, people, or open tasks.

Mitigation: Keep factual continuity in existing memory files and use this skill only for scoped execution lessons, corrections, and process patterns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sebclawops/skills/retrospective-agent)
- [Workflow](references/workflow.md)
- [Promotion Rules](references/promotion-rules.md)
- [Boundaries](references/boundaries.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with concise retrospective sections, lesson entries, and recommended workspace file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-first outputs; writes only visible retrospective notes when warranted by the current task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
