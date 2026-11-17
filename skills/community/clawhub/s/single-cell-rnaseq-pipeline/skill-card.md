## Description:

Generate single-cell RNA-seq analysis code templates for Seurat and Scanpy, supporting QC, clustering, visualization, and downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics analysts use this skill to generate Seurat or Scanpy pipeline templates for single-cell RNA-seq preprocessing, quality control, normalization, clustering, visualization, marker identification, batch correction, and downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene issues, including an scvi versus scvi-tools mismatch, could lead to unexpected installs or runtime failures.

Mitigation: Install in an isolated project environment, review dependency files before installation, and prefer pinned or locked dependency versions.

Risk: The generator writes files to a user-selected output path, which can overwrite existing work if the path is reused.

Mitigation: Review the output path before execution and generate into a clean project directory.

## Reference(s):

- [Batch Correction Methods Comparison](references/batch_correction_guide.md)
- [Scanpy Template Reference](references/scanpy_template.py)
- [Python Dependency Requirements](references/requirements.txt)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration]

**Output Format:** [Generated R and Python analysis templates, README markdown, and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes template files to the requested output path; supported options include tool, species, batch correction, trajectory, cell communication, differential expression, and spatial analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
