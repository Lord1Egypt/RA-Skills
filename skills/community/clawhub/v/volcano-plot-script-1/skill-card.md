## Description:

Generate R/Python code for volcano plots from DEG (Differentially Expressed Genes) analysis results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics analysts, and researchers use this skill to generate volcano plot scripts and outputs from differential gene expression result tables. It supports configurable columns, significance thresholds, gene labeling, colors, and optional significant-gene exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that exported R scripts can include unescaped user-controlled values.

Mitigation: Review generated R code before execution and use only trusted input values until R-string escaping is fixed.

Risk: The security review reports that output paths can overwrite arbitrary writable files.

Mitigation: Restrict output paths to a controlled workspace and review destinations before running the script.

Risk: The security guidance notes that dependencies are not pinned for reproducible or production use.

Mitigation: Pin and review Python and R dependencies before reproducible, automated, or production workflows.

## Reference(s):

- [Volcano Plot Script ClawHub page](https://clawhub.ai/aipoch-ai/skills/volcano-plot-script-1)
- [Volcano Plot Best Practices](references/best_practices.md)
- [Example DEG Data](references/example_deg_data.csv)
- [Example Genes to Label](references/markers.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code or shell commands, plus generated plot files, R scripts, or CSV outputs when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on supplied DEG data, column names, thresholds, gene labels, colors, and requested export paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
