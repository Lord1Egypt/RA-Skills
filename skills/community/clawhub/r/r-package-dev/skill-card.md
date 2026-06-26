## Description: <br>
Build, check, and submit R packages to CRAN or Bioconductor, including new-package setup, R CMD check fixes, CI, S4/Bioconductor design, roxygen2 documentation, visualization guidance, and submission troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuiweig](https://clawhub.ai/user/cuiweig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, harden, check, document, and submit R packages for CRAN or Bioconductor. It is especially relevant for package authors handling R CMD check, BiocCheck, GitHub Actions CI, S4 infrastructure, roxygen2 documentation, and publication-grade visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git history rewrite and force-push commands can rewrite shared repository history or overwrite collaborator work if run on the wrong branch or remote. <br>
Mitigation: Treat those commands as expert-only guidance: verify the target branch and remote, create a backup branch or tag, coordinate with collaborators, and prefer guarded commands such as force-with-lease where appropriate. <br>


## Reference(s): <br>
- [Bioconductor Submission Guide](references/bioconductor.md) <br>
- [CRAN Submission](references/cran.md) <br>
- [GitHub Actions CI for R Packages](references/github-actions.md) <br>
- [R Package Troubleshooting](references/troubleshooting.md) <br>
- [Publication-Grade R Visualization](references/visualization.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with R, YAML, bash, and checklist examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
