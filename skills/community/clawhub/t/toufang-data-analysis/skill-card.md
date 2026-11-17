## Description:

Analyzes Super Live, Taobao Live, and financial data files to calculate ROI, conversion, cost, revenue, and margin metrics and generate advertising performance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18262202398-star](https://clawhub.ai/user/18262202398-star)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, analysts, and commerce teams use this skill to process local advertising, livestream commerce, and financial spreadsheets for campaign ROI analysis, data quality checks, and optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include raw business data from local spreadsheets.

Mitigation: Use trusted input files, avoid opening generated HTML from untrusted spreadsheets until values are escaped, and review reports before sharing them.

Risk: The skill recursively loads CSV/XLSX files from the configured input directory without effective input-size limits.

Mitigation: Run it against a narrow, dedicated data directory and avoid folders containing unrelated, untrusted, or sensitive files.

Risk: Dependencies are specified as minimum versions rather than pinned versions.

Mitigation: Prefer a lockfile or pinned dependency set before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18262202398-star/skills/toufang-data-analysis)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated local HTML and CSV report files when the skill is executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local CSV/XLSX input files from a configured data directory and writes timestamped report files to a configured output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
