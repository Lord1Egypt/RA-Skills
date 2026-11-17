## Description:

R Machine Learning Workbench helps agents run local R workflows for data splitting, feature engineering, model training, model evaluation, survival machine learning, explainability, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanweisg](https://clawhub.ai/user/sanweisg)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, data scientists, and developers use this skill to build and compare R machine-learning pipelines for tabular and biomedical datasets, producing models, plots, predictions, result tables, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow may execute mutable third-party R package code.

Mitigation: Install only in an isolated R environment and review or pin dependencies before running the install command.

Risk: Input handling may allow untrusted datasets, attacker-supplied column names, or unsafe tags to affect local execution or output paths.

Mitigation: Avoid untrusted datasets, use simple alphanumeric tags, and review generated paths until path validation is added.

Risk: Generated output files may contain dataset-derived values, including raw train and test splits.

Mitigation: Treat the output directory as sensitive when working with private or regulated datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanweisg/skills/r-machine-learning)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; local R scripts generate CSV, RDS, PNG, PDF, HTML, and TeX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Rscript and an R environment with the documented machine-learning packages installed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
