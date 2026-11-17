## Description:

Guides brands through Xiaohongshu (Redbook) category analysis using public notes, creator profiles, and comments to produce evidence-bounded brand recommendations and GO/NO-GO decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, marketing, and strategy teams use this skill before entering a category, launching a product, or revising a Xiaohongshu content strategy to structure public-content sampling, creator/comment analysis, and an evidence-bounded investment decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supervised logged-in Xiaohongshu collection can create account, platform-terms, and compliance exposure.

Mitigation: Use only an authorized account, collect only public pages, keep scope and rate limits conservative, and stop rather than bypass login walls, CAPTCHA, or platform controls.

Risk: Collected creator and comment data may include identifiable public information despite de-identification goals.

Mitigation: Minimize retained fields, remove nicknames and avatars from deliverables, handle comments under applicable privacy requirements, and avoid sharing raw data unnecessarily.

Risk: The optional Agent-Reach installation path and dependencies are mutable external material.

Mitigation: Pin dependencies and separately review the external install content before client or business use; prefer manually inspected or built-in data paths when review is not possible.

Risk: Collected Markdown and report inputs may contain untrusted source material.

Mitigation: Sanitize collected Markdown before reuse, preserve evidence boundaries, and avoid executing or blindly copying content from source data.

Risk: Generated reports include required attribution text that may be inappropriate for some client deliverables.

Mitigation: Review the attribution requirement before delivery and either disclose it clearly or remove it where the release terms and client context allow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qomob/skills/xhs-track-analysis)
- [Methodology](artifact/references/methodology.md)
- [Data sources](artifact/references/data-sources.md)
- [Collection playbook](artifact/references/collection-playbook.md)
- [Table template](artifact/references/table-template.md)
- [Case study](artifact/references/case-study.md)
- [Collector README](artifact/scripts/collector/README.md)
- [Integrations README](artifact/scripts/integrations/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured tables, decision briefs, CSV/Markdown collection artifacts, and command/configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include evidence boundaries and may include GO/NO-GO recommendations; collected public creator/comment material should be treated as untrusted source data.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
