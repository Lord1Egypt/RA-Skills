## Description: <br>
Router NIMIMORE analyzes a query and selects an appropriate AI model tier to balance expected cost and performance across supported providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aichiafranco](https://clawhub.ai/user/aichiafranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to classify prompts and choose among economy, standard, and premium model options before dispatching work to a model provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If its selected model is connected to real provider calls, prompts may be sent to third-party providers. <br>
Mitigation: Avoid sending secrets or personal data unless the provider's data handling policy is acceptable for the intended use. <br>


## Reference(s): <br>
- [Router NIMIMORE ClawHub Page](https://clawhub.ai/aichiafranco/router-nimimore) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local model-selection recommendations and routing analysis; no persistence or provider calls are evidenced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
