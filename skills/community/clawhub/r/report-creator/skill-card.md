## Description: <br>
Generates self-contained HTML reports, business summaries, research documents, and KPI dashboards from raw notes, URLs, or .report.md outlines, with planning, theming, review, and export-image routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaisersong](https://clawhub.ai/user/kaisersong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to turn notes, source documents, URLs, or approved report IR into polished single-file HTML reports. It also supports report planning, theme previews, one-pass review, validation gates, and image export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may execute JavaScript from public CDNs when assets are not bundled. <br>
Mitigation: Use the bundled or offline output path for confidential reports and inspect generated HTML before sharing. <br>
Risk: Generated reports include edit, save, and export controls that may be easy to miss during review. <br>
Mitigation: Review the final HTML shell controls and run the provided quality gates before publishing or distributing a report. <br>
Risk: The README describes a Telegram sharing workflow for IM-friendly report images. <br>
Mitigation: Do not rely on Telegram delivery unless a separate trusted integration sends the report with explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaisersong/report-creator) <br>
- [README](README.md) <br>
- [When To Use](examples/when-to-use.md) <br>
- [Do Not Use](examples/do-not-use.md) <br>
- [IR Contract](references/ir-contract.md) <br>
- [Generate Flow](references/generate-flow.md) <br>
- [Review Checklist](references/review-checklist.md) <br>
- [HTML Shell Template](references/html-shell-template.md) <br>
- [Rendering Rules](references/rendering-rules.md) <br>
- [Theme Routing](references/theme-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, .report.md intermediate representations, self-contained HTML files, and shell commands for validation or export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include inline JavaScript, public CDN assets when not bundled, export controls, and machine-readable report metadata.] <br>

## Skill Version(s): <br>
1.23.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
