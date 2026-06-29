## Description: <br>
R Machine Learning Workbench runs local R workflows for data splitting, feature engineering and selection, model training and tuning, evaluation, explainability, survival analysis, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanweisg](https://clawhub.ai/user/sanweisg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and biomedical or bioinformatics researchers use this skill to run R-based machine-learning pipelines, compare models, evaluate predictions, explain model behavior, and generate shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install command can add many R packages from CRAN and GitHub to the local R environment. <br>
Mitigation: Install and run the skill only in an environment where adding those dependencies is acceptable. <br>
Risk: Generated reports, plots, tables, predictions, and model objects can contain dataset-derived information. <br>
Mitigation: Run the workflow on copies of sensitive datasets and review the output folder before sharing artifacts. <br>
Risk: Calibration analysis depends on predicted probabilities and ground-truth rows matching correctly. <br>
Mitigation: Verify calibration inputs have matching row order and row counts before relying on the calibration results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sanweisg/r-machine-learning) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands plus local files such as CSV tables, RDS model objects, HTML or PDF reports, and PDF, PNG, or SVG plots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are saved under output/plots, output/models, output/predictions, output/reports, and output/tables when the bundled launchers are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
