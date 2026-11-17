## Description:

VecML AutoML trains machine learning models from CSV files, runs predictions, lists models, and shows validation metrics and feature importance through a Python pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinle2](https://clawhub.ai/user/tinle2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to train classification or regression models from CSV datasets, generate predictions, and inspect validation metrics or feature importance without building a custom notebook workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected CSV data and the VecML API key to a VecML endpoint controlled by environment configuration.

Mitigation: Use only non-sensitive or approved datasets, keep VECML_API_KEY protected, and leave VECML_API_URL unset or set it only to a trusted HTTPS VecML endpoint.

## Reference(s):

- [VecML AutoML API documentation](https://aidb.vecml.com/docs/site/automl_api/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and optional CSV prediction files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Training output includes status text, validation metrics, and feature importance; prediction runs may write a *_predictions.csv file.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
