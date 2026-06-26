## Description: <br>
Provides a framework for assessing prediction uncertainty through information completeness, prediction type, confidence scoring, and risk notices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keys-li](https://clawhub.ai/user/keys-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when answering predictive or judgment-heavy questions to estimate confidence, surface uncertainty, and decide when to seek more information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat confidence scores as expert advice for medical, legal, financial, safety-critical, or other high-stakes decisions. <br>
Mitigation: Use the skill as reasoning support only and require qualified expert review before acting on high-stakes outputs. <br>
Risk: The broad prediction and judgment posture can be overapplied to tasks where uncertainty scoring is not enough to establish reliability. <br>
Mitigation: Apply it when uncertainty assessment is relevant, state key assumptions and information gaps, and seek additional evidence when confidence is low. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keys-li/self-aware-prediction-system) <br>
- [Publisher Profile](https://clawhub.ai/user/keys-li) <br>
- [Uncertainty Assessment Standards](references/standards.md) <br>
- [Usage Guide](assets/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with confidence scores, risk notices, and optional Python helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces confidence scores, uncertainty notices, and risk levels for prediction or judgment tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
