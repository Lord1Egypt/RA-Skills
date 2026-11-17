## Description:

Generates Chinese-language technology insight reports covering topic selection, patent and market evidence gathering, HTML report authoring, quality checks, and publication review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, IP strategy teams, and external developers use this skill to create structured technology insight reports that combine patent, market, research, policy, standards, and competitive intelligence. It is intended for HTML report generation and quality review workflows, not simple single-patent lookup or non-patent market summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports reference Chart.js from a third-party CDN, which can create availability, confidentiality, or supply-chain concerns for sensitive report workflows.

Mitigation: For confidential or controlled environments, bundle Chart.js locally or add verified SRI and CSP controls, and retain the offline fallback tables required by the artifact.

Risk: Live patent and research conclusions depend on appropriate PatSnap MCP and web search access.

Mitigation: Confirm the required PatSnap authorization and web search availability before using the skill for evidence-backed conclusions; without those tools, treat output as an analysis framework only.

Risk: Local quality scripts can produce misleading validation results if run against the wrong report file or an incomplete draft.

Mitigation: Run the scripts only against the intended report HTML and pair script output with the bundled publication checklist before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/tech-insight-report)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [PatSnap open platform](https://open.zhihuiya.com/)
- [Chart.js runtime referenced by HTML template](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)
- [HTML skeleton template](artifact/references/html_skeleton_template.html)
- [Quality checklist](artifact/references/quality_checklist.md)
- [Section 4 exhaustive patent search specification](artifact/references/s4_exhaustive_search_spec.md)
- [Cross-section sync table template](artifact/references/sync_table_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language workflow guidance, Markdown checklists, HTML report templates, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are expected to use a fixed ten-section HTML structure, Chart.js visualizations, offline fallback tables, and local quality-check scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
