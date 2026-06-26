## Description: <br>
Uploads CSV data and generates common ggplot2 charts, including scatter plots, bar charts, box plots, line charts, histograms, facet plots, and publication-style figures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenthompson2088](https://clawhub.ai/user/kenthompson2088) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to turn CSV files into ggplot2 visualizations without writing plotting code. It is suited for quick exploratory charts and repeatable chart generation from tabular data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local run path may install ggplot2 from CRAN when the package is missing. <br>
Mitigation: Preinstall or pin R dependencies in controlled environments before running the skill. <br>
Risk: The security guidance notes that run_plot.R, Dockerfile, and Singularity.def are not present in the release evidence even though documented execution paths depend on them. <br>
Mitigation: Verify those assets from a trusted source before relying on local, Docker, or Singularity execution. <br>
Risk: The Docker build script can push an image when DOCKER_USERNAME is set. <br>
Mitigation: Review the target registry and authentication state, or unset DOCKER_USERNAME, before running the Docker publishing path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenthompson2088/r-ggplot-quickplot) <br>
- [Input data format](input/DATA_FORMAT.md) <br>
- [R Project CRAN](https://cran.r-project.org/) <br>
- [Docker installation documentation](https://docs.docker.com/get-docker/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chart image files with command-line status text and configuration-driven options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected chart outputs include PNG by default, with documented support for PDF and SVG configuration.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
