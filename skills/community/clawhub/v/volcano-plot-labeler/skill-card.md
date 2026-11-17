## Description:

Automatically label top significant genes in volcano plots with a repulsion algorithm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ec-cyber258](https://clawhub.ai/user/ec-cyber258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data scientists, and bioinformatics analysts use this skill to generate volcano plots that label the most significant genes while reducing label overlap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may change behavior or introduce vulnerable packages over time.

Mitigation: Install in a virtual environment or container with reviewed pinned versions of pandas, numpy, and matplotlib; remove scipy unless it is needed.

Risk: The script reads user-provided CSV or TSV files and writes output to the path supplied by the user.

Mitigation: Use trusted input files and choose output paths carefully before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ec-cyber258/skills/volcano-plot-labeler)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands]

**Output Format:** [PNG, PDF, or SVG plot files; Python API returns a matplotlib Figure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads CSV or TSV differential expression data and writes the plot to the requested output path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
