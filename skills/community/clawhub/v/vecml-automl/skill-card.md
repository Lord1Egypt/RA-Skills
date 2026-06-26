## Description: <br>
VecML AutoML trains models from CSV data, runs predictions, reports validation metrics, and shows feature importance through a one-command Python pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinle2](https://clawhub.ai/user/tinle2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides CSV data and wants to train a VecML classification or regression model, run predictions, list trained models, or inspect feature importance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected CSV rows, labels, and prediction inputs are sent to VecML during training and prediction. <br>
Mitigation: Use only datasets approved for VecML, avoid sensitive or regulated data unless approved, and confirm the target column plus project, collection, and model names before running. <br>
Risk: The skill requires a VecML API key and can use an alternate VECML_API_URL endpoint. <br>
Mitigation: Use a revocable VecML API key and leave VECML_API_URL unset unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [VecML AutoML API Documentation](https://aidb.vecml.com/docs/site/automl_api/) <br>
- [ClawHub Skill Page](https://clawhub.ai/tinle2/vecml-automl) <br>
- [Publisher Profile](https://clawhub.ai/user/tinle2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV prediction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and VECML_API_KEY; prediction runs write a *_predictions.csv file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
