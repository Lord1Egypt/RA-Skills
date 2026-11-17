## Description:

This skill guides an agent to produce Chinese-first spatiotemporal research reports using sourced timelines, cross-sectional comparisons, confidence-labeled convergence judgments, and report/PDF templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users, research analysts, and developers use this skill to structure research on products, companies, technologies, people, or policy topics that need both a time-based history and a current ecosystem comparison. It supports sourced Chinese Markdown reports, confidence-labeled forecasts, and PDF-oriented delivery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can execute Python from another local skill path.

Mitigation: Install only in a trusted local skill environment and review the referenced dependency skill before use.

Risk: Research queries and results may be retained in a local cache under ~/.hermes.

Mitigation: Avoid sensitive research subjects unless local retention is acceptable, or configure and clean a dedicated cache directory.

Risk: The workflow may use network search and GitHub CLI access during data collection.

Mitigation: Run it in an environment where outbound network and GitHub CLI use are approved and observable.

Risk: The skill is Chinese-first and may not fit all review audiences.

Mitigation: Confirm language expectations before relying on outputs for stakeholder review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingsunzhang2026-oss/skills/spatiotemporal-analysis)
- [Methodology](artifact/references/methodology.md)
- [Data Source Guidance](artifact/references/data_sources.md)
- [Output Conventions and Source Quirks](artifact/references/output-conventions-and-source-quirks.md)
- [Writing Baseline](artifact/references/writing_baseline.md)
- [Chinese PDF Recipe](artifact/references/markdown-to-pdf-zh.md)
- [Convergence Probability Table Template](artifact/templates/convergence_table.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-first Markdown research reports, JSON report templates, Python command output, and PDF-oriented Markdown/LaTeX guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize source URLs, timestamps, confidence labels, concise conclusions, and optional local cache use.]

## Skill Version(s):

2.0.2 (source: server release metadata and changelog; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
