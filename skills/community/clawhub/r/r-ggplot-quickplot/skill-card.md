## Description:

R ggplot Quickplot helps an agent generate common ggplot2 charts from uploaded CSV data, with documented local, Docker, and Singularity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenthompson2088](https://clawhub.ai/user/kenthompson2088)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and data science users can use this skill to turn CSV datasets into scatter plots, bar charts, box plots, line plots, histograms, faceted plots, and publication-style ggplot2 outputs. It is useful when an agent needs to provide plotting commands, configuration guidance, or generated chart files without hand-authoring R visualization code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local workflow may install the ggplot2 R package from the network at runtime.

Mitigation: Use a controlled environment with reviewed or pinned R dependencies before installing or running the skill.

Risk: The container workflow is described by the skill but the release evidence reports it as incomplete or requiring verification of missing build/runtime files.

Mitigation: Verify required container files and prefer a reviewed container image before relying on Docker or Singularity execution.

Risk: Running the skill from a broad working directory can expose unrelated local files to container mounts or script execution.

Mitigation: Run it from a dedicated directory that contains only the intended CSV input and output folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenthompson2088/skills/r-ggplot-quickplot)
- [R Project CRAN](https://cran.r-project.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Docker installation documentation](https://docs.docker.com/get-docker/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; generated chart files are PNG by default with documented PDF and SVG options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an output directory containing up to nine chart files from a CSV input.]

## Skill Version(s):

3.1.0 (source: server release metadata and root artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
