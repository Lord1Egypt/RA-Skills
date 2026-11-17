## Description:

Clusters user feedback into a frequency-weighted requirement evidence table that preserves representative quotes and avoids overstating weak evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, support teams, and operators use this skill to turn pasted user feedback from reviews, support records, surveys, or chats into a structured evidence table for requirement triage and prioritization discussion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User feedback can contain personal or sensitive information.

Mitigation: Remove or mask sensitive details before pasting feedback into an agent.

Risk: Small samples or vague comments can be overstated as broad product demand.

Mitigation: Keep the skill's evidence-strength labels, sample-size caveats, and weak-evidence wording in the final report.

Risk: Generated prioritization suggestions can be mistaken for final roadmap decisions.

Mitigation: Treat priority ordering as discussion support and keep implementation cost marked for engineering assessment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyuming0823/skills/ym-feedback-evidence-triage)
- [Server-resolved Source Repository](https://github.com/liuyuming0823/ym-feedback-evidence-triage)
- [Evidence Rules](references/evidence-rules.md)
- [Evidence Table Template](templates/evidence-table-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evidence report with structured tables and short explanatory sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses evidence-strength labels, sample-size caveats, representative original quotes, conflict reporting, and implementation-cost placeholders that require engineering assessment.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
