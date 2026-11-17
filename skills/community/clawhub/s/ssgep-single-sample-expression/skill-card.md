## Description:

Guides agents through RNA-seq expression profiling for single-sample or replicated experiments, including quality control, DEG analysis, GO/KEGG enrichment, WGCNA, SNP analysis, 600 DPI figures, report outputs, and Shiny artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bsk-drs](https://clawhub.ai/user/bsk-drs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and run RNA-seq expression-profile workflows for plant or similar transcriptomic datasets, including both single-sample no-replicate and biologically replicated modes. It helps an agent propose setup steps, shell/R/Python commands, analysis criteria, output packaging, and publication-style report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run long Bash, R, and Python analysis commands and write report outputs into the working project.

Mitigation: Run it in a project directory or isolated environment with intended input data, and require confirmation before launching long workflows or writing generated reports.

Risk: Package installation guidance includes unpinned R and Python package installs, which can change dependency behavior over time.

Mitigation: Review installation commands before execution and prefer pinned lockfiles or a controlled environment for repeatable analyses.

Risk: Single-sample no-replicate DEG analysis uses an approximate fixed-dispersion and fold-change approach, so statistical claims can be weaker than replicated designs.

Mitigation: Treat p-values as ranking support, disclose the no-replicate limitation, and validate key genes with qRT-PCR or an independent dataset when making biological claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bsk-drs/skills/ssgep-single-sample-expression)
- [Publisher profile](https://clawhub.ai/user/bsk-drs)
- [R for Windows](https://cloud.r-project.org/bin/windows/base/)
- [RStudio Desktop](https://posit.co/download/rstudio-desktop/)
- [Python for Windows](https://www.python.org/downloads/windows/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, R, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local analysis files, figures, HTML/DOCX/PPTX reports, tables, and Shiny app artifacts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
