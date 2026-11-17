## Description:

Comprehensive data analysis workflow for CSV files with interactive guidance and flexible output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide CSV data analysis, data cleaning, exploratory analysis, visualization, insight generation, and report or dashboard delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify the Python environment by installing analysis packages.

Mitigation: Run it in an isolated environment and preinstall reviewed dependencies when possible.

Risk: Generated HTML reports can contact external CDNs for Chart.js and Tailwind CSS.

Mitigation: Use Markdown output for sensitive data, or review and self-host required assets before sharing HTML reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yz6214589-hash/skills/yz6214589-hash-data-analysis)
- [Chart.js CDN script used by generated HTML reports](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)
- [Tailwind CSS CDN script used by generated HTML reports](https://cdn.tailwindcss.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, interactive HTML reports, dashboard files, charts, cleaned CSV data, and analysis guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create timestamped data-analysis-results directories containing reports, charts, cleaned data, and optional analysis code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
