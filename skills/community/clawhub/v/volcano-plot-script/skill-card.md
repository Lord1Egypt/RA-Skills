## Description:

Generates R/Python code and runnable plotting workflows for volcano plots from differential gene expression analysis results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ec-cyber258](https://clawhub.ai/user/ec-cyber258)

### License/Terms of Use:

MIT-0

## Use Case:

Bioinformatics developers and analysts use this skill to create publication-ready volcano plots, classify differentially expressed genes, label genes of interest, and export supporting plot or gene-list files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional R export can place user-controlled values into executable R code.

Mitigation: Use trusted inputs, avoid --export-r for untrusted arguments or paths, and review generated .R files before execution.

Risk: The script reads local DEG input files and writes plot, script, or gene-list outputs in the workspace.

Mitigation: Run it in a controlled workspace with isolated or pinned dependencies and review output paths before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ec-cyber258/skills/volcano-plot-script)
- [Volcano Plot Best Practices](references/best_practices.md)
- [Example DEG Data](references/example_deg_data.csv)
- [Example Genes to Label](references/markers.txt)

## Skill Output:

**Output Type(s):** [code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline commands, plus generated Python/R code paths and plot or CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate PNG, PDF, or SVG volcano plots, optional R scripts, and optional significant-gene CSV exports.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
