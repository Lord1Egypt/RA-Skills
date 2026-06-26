## Description: <br>
Interact with R and RStudio environments for scientific research tasks including creating projects, running analyses, managing dependencies, and generating publication-quality plots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, data scientists, and developers use this skill to scaffold reproducible R projects, run R scripts and R Markdown analyses, debug package environments, and generate publication-ready plots and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running analyses can execute local R code and write project files. <br>
Mitigation: Review the project and scripts before execution, choose an explicit project directory, and use a dedicated output path for generated files. <br>
Risk: Package installation, report rendering, Git initialization, and project scaffolding can modify the local environment or workspace. <br>
Mitigation: Run the skill in a controlled workspace, review generated installation commands and file changes, and avoid using untrusted or sensitive data without prior inspection. <br>


## Reference(s): <br>
- [Rstudio Research Agent README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/JackKuo666/rstudio-research-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with R code, shell commands, file paths, generated project files, reports, tables, and plot artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include R project scaffolds, renv configuration, RStudio project files, rendered R Markdown or Quarto reports, analysis summaries, and exported plot files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
