## Description: <br>
Generates customizable R or Python volcano plot scripts and local plot outputs from DEG analysis results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EC-cyber258](https://clawhub.ai/user/EC-cyber258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics researchers and developers use this skill to create publication-ready volcano plots, classify significant genes, label genes of interest, and export supporting plot or gene-list files from differential expression data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned Python dependencies may resolve to different versions over time. <br>
Mitigation: Install dependencies in a virtual environment and pin or review package versions for reproducible work. <br>
Risk: The local plotting script reads DEG input files and writes plots, scripts, or gene lists. <br>
Mitigation: Run it only on intended project files and keep generated outputs in a project directory. <br>
Risk: Exported R scripts are generated files that may be executed separately. <br>
Mitigation: Review any exported R script before running it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EC-cyber258/volcano-plot-script) <br>
- [Volcano Plot Best Practices](references/best_practices.md) <br>
- [Example DEG Data](references/example_deg_data.csv) <br>
- [Example Gene Markers](references/markers.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python or R code snippets and local plot, script, or CSV outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include PNG, PDF, SVG, R script, and significant-gene CSV files depending on selected options.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
