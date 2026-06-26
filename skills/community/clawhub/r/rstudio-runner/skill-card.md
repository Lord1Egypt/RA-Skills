## Description: <br>
AI-powered bioinformatics analysis platform that detects sequencing data, generates R/RStudio analysis scripts, organizes outputs, and produces Chinese analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingzhangmeng](https://clawhub.ai/user/lingzhangmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan and run local R/RStudio bioinformatics workflows for sequencing data, including scRNA-seq and bulk sequencing analysis. It helps organize project folders, generate R scripts, save plots and tables, and create Chinese-language reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated R scripts or analysis steps may be incorrect or unsuitable for a specific dataset. <br>
Mitigation: Review generated R scripts, package choices, parameters, and output paths before execution. <br>
Risk: Bioinformatics reports, logs, CSV files, and RDS objects may contain sensitive biomedical data. <br>
Mitigation: Use a dedicated project folder, restrict access to generated outputs, and treat reports and intermediate files as sensitive. <br>
Risk: Local workflow execution can write many files into structured subfolders. <br>
Mitigation: Confirm the intended working directory and output locations before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingzhangmeng/rstudio-runner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lingzhangmeng) <br>
- [Artifact homepage](https://clawhub.ai/skills/k97f5d8d367me4186h0d5j1jb583st34) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with R/RStudio scripts, shell commands, file organization plans, and report descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project outputs such as R scripts, plots, CSV/TXT tables, RDS objects, logs, and HTML/PDF reports.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
