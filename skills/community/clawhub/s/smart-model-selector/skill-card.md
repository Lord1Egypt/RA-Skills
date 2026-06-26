## Description: <br>
Smart Model Selector routes a task to an appropriate Qwen model based on task content, prior local feedback, and simple override commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billhandsome52](https://clawhub.ai/user/billhandsome52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this hook to recommend qwen3.5-plus, qwen-max, or qwen-coder-plus for an incoming task, with commands for manual selection, ratings, reset, and usage statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local task history may include prompt text saved in the skill's SQLite database. <br>
Mitigation: Avoid using the skill with secrets, private code, or personal data unless local retention is acceptable; delete data/model_selection.db or add redaction and retention controls. <br>
Risk: Automatic routing can recommend a model that is weaker or more expensive than intended for a given task. <br>
Mitigation: Use /model-use to override the recommendation and /model-rate to provide feedback that improves later routing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/billhandsome52/smart-model-selector) <br>
- [Project repository listed in artifact metadata](https://github.com/xuyun/smart-model-selector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown-formatted model recommendations and command replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes selected model, selection reason, usage statistics, and rating/reset acknowledgements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
