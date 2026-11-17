## Description:

Calculates Spearman correlations between two tabular datasets and outputs FDR-adjusted results for microbiome-style analyses such as family abundance versus environmental factors or functional gene tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and microbiome researchers use this skill to compare matched feature tables, run single-file or batch Spearman correlation analysis, apply Benjamini-Hochberg FDR correction, and summarize significant positive and negative associations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Correlation results may be scientifically unstable for small sample sizes or affected by undefined correlations for constant rows.

Mitigation: Review the generated summaries and spreadsheets before relying on results, especially when sample counts are small or NaN values appear.

Risk: The workflow reads and analyzes user-specified files or folders.

Mitigation: Point the agent only at directories containing data intended for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zd200572/skills/spearman-correlation)
- [Publisher profile](https://clawhub.ai/user/zd200572)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files]

**Output Format:** [Markdown guidance and summaries, with generated Excel (.xlsx) result files when analysis is performed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excel workbooks contain correlation, pvalue, and FDR sheets; summaries include raw and FDR significance counts plus top positive and negative associations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
