## Description: <br>
Generate single-cell RNA-seq analysis code templates for Seurat and Scanpy, supporting QC, clustering, visualization, and downstream analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics analysts use this skill to generate local single-cell RNA-seq workflow templates for preprocessing, quality control, normalization, clustering, visualization, marker analysis, batch correction, and optional downstream analyses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated analysis templates may be run against sensitive genomics datasets in a local environment. <br>
Mitigation: Run the skill and generated scripts in an isolated analysis environment and treat all input datasets and output files as sensitive local data. <br>
Risk: The generated workflows rely on Python and R bioinformatics dependencies that may change over time. <br>
Mitigation: Review and pin dependencies before installation, and validate generated templates on non-sensitive test data before production analysis. <br>
Risk: Template output can write files to the selected output directory. <br>
Mitigation: Generate templates into a dedicated workspace directory and review paths before executing generated code. <br>


## Reference(s): <br>
- [Batch Correction Methods Comparison](references/batch_correction_guide.md) <br>
- [Scanpy Template Reference](references/scanpy_template.py) <br>
- [Python dependency requirements](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Generated R and Python script templates with Markdown README guidance and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated templates to a user-selected local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
