## Description:

Builds a structured Markdown work handover pack from scattered responsibilities, open items, permissions, contacts, risks, and tacit knowledge while marking missing information instead of inventing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill when preparing job handovers, role transitions, long leave coverage, or project transfers. It turns scattered work notes into a nine-section handover document covering duties, open work, recurring tasks, permissions, contacts, tacit knowledge, risks, and a transition timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include passwords, tokens, or unredacted confidential business context in handover material.

Mitigation: Do not include passwords, tokens, or unredacted confidential material; redact sensitive details before generating a handover document.

Risk: Optional saved drafts may retain business handover context locally.

Mitigation: Only save handover drafts when local storage of that business context is acceptable, and remove sensitive details before saving.

Risk: Incomplete source notes could be mistaken for complete handover facts.

Mitigation: Review placeholders and follow-up questions before sharing the handover pack, and confirm missing duties, contacts, systems, and tacit knowledge with the source owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-work-handover-pack)
- [Server-resolved GitHub source](https://github.com/liuyuming0823/ym-work-handover-pack)
- [Information Gap Eight-Dimension Checklist](references/信息缺口八维度清单.md)
- [Tacit Knowledge Question Bank](references/隐性知识提问库.md)
- [Work Handover Pack Template](templates/交接包模板.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown handover document with tables, placeholders, and follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed nine-section structure; omits passwords and marks missing or sensitive details for user review.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
