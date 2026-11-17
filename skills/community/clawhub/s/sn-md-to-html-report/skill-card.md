## Description:

Converts long Markdown reports into editorially designed, self-contained HTML feature pages while preserving source facts, evidence, and conclusion strength.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, analysts, designers, and developers use this skill when an agent needs to turn a report-like Markdown document into a polished, shareable HTML page. It is intended for long-form reports, research notes, industry analysis, strategy memos, technical white papers, reviews, and weekly reports where layout, evidence order, and visual design matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can expose confidential or regulated report content if the source document is sensitive and the page is shared broadly.

Mitigation: Review the source report and generated HTML for confidentiality, regulated data, and sharing permissions before distribution.

Risk: Editorial restructuring and visual emphasis can accidentally overstate a claim, omit a limitation, or make a visual metaphor look like evidence.

Mitigation: Use the skill's required fact-fidelity review to check that figures, sources, hedges, limitations, and conclusion strength still match the original report.

## Reference(s):

- [Aesthetic Direction](references/01-aesthetic-direction.md)
- [Layout and Content Design](references/02-layout-and-content-design.md)
- [Design Contract](references/03-design-contract.md)
- [Review Angles](references/04-review-angles.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, files]

**Output Format:** [Markdown plan plus a self-contained HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a plan.md design contract before HTML creation and expects the final HTML to be reviewable as a single file.]

## Skill Version(s):

2026.8.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
