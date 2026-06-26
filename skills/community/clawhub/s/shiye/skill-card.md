## Description: <br>
Shiye runs Kimi, GLM, and Qwen as three AI reviewers for documents, code, resumes, and other text, then reports score comparisons, deduction details, consensus issues, and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlarkspur](https://clawhub.ai/user/vlarkspur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, reviewers, and agents use this skill to evaluate documents, code, resumes, email, presentation text, and similar content through three model-based reviewers. It is intended to compare scores, surface deduction reasons, identify consensus problems, and suggest improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed documents, code, resumes, or other text can be sent to the configured external API provider. <br>
Mitigation: Use the skill only when external processing is approved, and avoid sending secrets, proprietary code, regulated data, resumes, or confidential documents unless that use is authorized. <br>
Risk: The script supports placing an API key directly in source code. <br>
Mitigation: Prefer SHIYE_API_KEY and SHIYE_API_BASE environment variables, and do not commit or share a modified script containing credentials. <br>
Risk: When no criteria file is provided, the skill auto-generates criteria by sending a sample of the reviewed content to the model API. <br>
Mitigation: Provide an explicit criteria file for sensitive material so criteria generation does not send an additional sample before scoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlarkspur/shiye) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Console text with score tables, deduction details, reviewer diagnostics, consensus analysis, and short improvement guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured API key; reviewed content is sent to the configured API provider and is truncated to 16000 characters for scoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
