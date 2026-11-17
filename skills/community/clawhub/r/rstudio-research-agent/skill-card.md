## Description:

Interact with R and RStudio environments for scientific research tasks including creating projects, running analyses, managing dependencies, and generating publication-quality plots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Researchers, data scientists, and developers use this skill to create reproducible R projects, run R scripts and R Markdown or Quarto analyses, troubleshoot package environments, and generate publication-ready figures and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: R scripts, .Rprofile files, renv activation, R Markdown, and Quarto can execute arbitrary code, install packages, or write files.

Mitigation: Use the skill only with trusted projects and review scripts, report sources, and package-install actions before execution.

Risk: The skill can create or modify project files, reports, figures, tables, model files, and environment configuration.

Mitigation: Run it in a version-controlled workspace and review generated file changes before relying on or sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackkuo666/skills/rstudio-research-agent)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with R code blocks, shell commands, generated file paths, and saved analysis artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify R project files, reports, figures, tables, model files, renv.lock, .Rprofile, .Rproj, and .gitignore.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
