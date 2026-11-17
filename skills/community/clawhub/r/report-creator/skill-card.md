## Description:

Creates polished single-file HTML reports, business summaries, data dashboards, and research documents from notes, data, URLs, or approved report plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers use this skill to turn source material into readable HTML reports with structured summaries, KPI blocks, charts, tables, timelines, themes, review passes, and optional image export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports load mutable third-party browser code by default, which can expose report contents if that code is compromised.

Mitigation: For sensitive reports, require bundled or offline assets, pin and verify CDN scripts, and avoid opening generated reports where third-party network loads are unacceptable.

Risk: Report outputs may contain confidential data and can be combined with messaging tools that send content externally.

Mitigation: Decide confidentiality requirements before installation and only combine this skill with Telegram or other messaging tools when external sharing is intended.

Risk: Generated report facts, numbers, and interpretations may be incomplete when source data is missing or ambiguous.

Mitigation: Review generated reports before use and require missing values to remain explicit placeholders rather than fabricated facts or metrics.

## Reference(s):

- [Report Creator ClawHub page](https://clawhub.ai/kaisersong/skills/report-creator)
- [Reference index](references/INDEX.md)
- [IR contract](references/ir-contract.md)
- [Generate flow](references/generate-flow.md)
- [Review checklist](references/review-checklist.md)
- [Theme routing](references/theme-routing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated .report.md IR, self-contained HTML files, and optional exported images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports can include machine-readable summaries, section annotations, component data, themes, export controls, and validation metadata.]

## Skill Version(s):

1.23.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
