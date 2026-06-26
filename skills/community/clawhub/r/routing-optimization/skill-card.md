## Description: <br>
Analyzes dispatch logs to measure routing hit rates and accuracy, compare routing strategies, and produce recommendations for improving routing rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who maintain agent dispatch systems use this skill to review routing logs, compare routing strategies with A/B tests, and generate recommendations before changing routing rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dispatch logs may contain sensitive user prompts or operational data. <br>
Mitigation: Confirm which logs will be analyzed and avoid storing raw sensitive prompts when possible. <br>
Risk: Suggested routing-rule changes could reduce routing accuracy or create unintended dispatch behavior. <br>
Mitigation: Review recommendations manually, test changes in staging, and keep automatic optimization disabled unless explicitly approved. <br>
Risk: Broad keywords can produce noisy or incorrect routing matches in production. <br>
Mitigation: Narrow broad keywords and validate routing behavior with representative test queries before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/routing-optimization) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Routing optimization configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, PowerShell, JSON, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis patterns, example functions, configuration defaults, metric definitions, and human-reviewed optimization suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact config version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
