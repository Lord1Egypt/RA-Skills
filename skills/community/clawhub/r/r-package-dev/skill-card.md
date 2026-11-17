## Description:

Build, check, and submit R packages to CRAN or Bioconductor, including package skeletons, documentation, checks, CI, S4/Bioconductor patterns, visualization guidance, and submission troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiweig](https://clawhub.ai/user/cuiweig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and R package maintainers use this skill to create R packages from scratch, resolve R CMD check and BiocCheck issues, configure CI, and prepare CRAN or Bioconductor submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git history rewrite examples can damage collaboration history or overwrite remote branches if copied without preparation.

Mitigation: Only rewrite history with backups, a clean current branch, collaborator agreement, and a clear recovery plan; avoid force pushes unless necessary.

Risk: Unpinned CI actions and dependency installation examples can reduce reproducibility or supply-chain control.

Mitigation: Pin GitHub Actions versions and dependency snapshots when reproducible or controlled builds are required.

## Reference(s):

- [Bioconductor Submission Guide](references/bioconductor.md)
- [CRAN Submission](references/cran.md)
- [GitHub Actions CI for R Packages](references/github-actions.md)
- [R Package Troubleshooting](references/troubleshooting.md)
- [Publication-Grade R Visualization](references/visualization.md)
- [Bioconductor Package Guidelines](https://contributions.bioconductor.org/develop-overview.html)
- [Bioconductor Package Submission](https://contributions.bioconductor.org/submission-overview.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline R, YAML, shell, and checklist examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory package-development instructions and templates; users should review commands before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
