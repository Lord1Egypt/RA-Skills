## Description:

Retro a campaign against its goals and propose the next testable experiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and business operations teams use this skill to review a completed campaign against its goals, separate evidence-backed findings from assumptions, and plan three measurable experiments for the next campaign.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad campaign-summary wording can invoke the skill when the user needs a non-campaign summary or prefers English output.

Mitigation: Clarify the campaign scope and preferred language when user intent is ambiguous.

Risk: Incomplete campaign goals or result data can make conclusions qualitative or assumption-based.

Mitigation: Mark missing goals as assumptions, label unsupported conclusions as lacking data support, and list data gaps in the output.

## Reference(s):

- [GitHub source repository](https://github.com/liuyuming0823/ym-campaign-retro-next)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-campaign-retro-next)
- [Attribution rules](references/attribution-rules.md)
- [Experiment template](references/experiment-template.md)
- [Campaign retrospective template](templates/retro-template.md)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown campaign retrospective with tables, attribution labels, data gaps, and structured experiment sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided campaign goals and result data; no external data retrieval.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
