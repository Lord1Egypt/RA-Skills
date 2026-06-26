## Description: <br>
Generates R/Python code and local plotting outputs for volcano plots from differential gene expression analysis results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, bioinformaticians, and data analysts use this skill to generate publication-ready volcano plots from DEG result tables, label genes of interest, and optionally export plotting scripts or significant gene lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running local plotting code on user-selected DEG files may execute dependencies or process files outside the intended workflow. <br>
Mitigation: Install and run the skill in a virtual environment, use real CSV/TSV DEG inputs, and review or pin dependencies when reproducibility matters. <br>
Risk: Incomplete documentation examples could lead users to pass free text where the script expects a file path. <br>
Mitigation: Treat --input as a path to a validated CSV/TSV file and confirm required column names before execution. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/aipoch-ai/volcano-plot-script-1) <br>
- [Volcano Plot Best Practices](references/best_practices.md) <br>
- [Example DEG Data](references/example_deg_data.csv) <br>
- [Example Genes to Label](references/markers.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python/R code, shell commands, and generated plot or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce PNG/PDF/SVG plots, an optional R script, and optional significant-gene CSV output from local CSV/TSV inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
