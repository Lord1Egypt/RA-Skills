## Description: <br>
Route user tasks to the most relevant skills using a layered taxonomy, risk model, and minimum-necessary-loading strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzk332266](https://clawhub.ai/user/wzk332266) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose the most relevant skill for a task, classify new skills, manage routing policy, and apply risk-aware minimum-necessary-loading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can record local routing decisions and maintain a local skill index. <br>
Mitigation: Install it only when local routing governance records are desired, and review generated reports before relying on them for routing priority. <br>
Risk: The intake workflow can download external skills into a local inbox. <br>
Mitigation: Use intake deliberately, review downloaded skills before loading or executing them, and avoid granting risky operations to newly downloaded skills without explicit approval. <br>
Risk: The cleanup workflow can delete the local skills inbox. <br>
Mitigation: Run cleanup only after the inbox has been reviewed and organized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzk332266/skill-taxonomy-router-pro) <br>
- [Session layer](references/session-layer.md) <br>
- [Skill classification schema](references/skill-classification-schema.md) <br>
- [Risk/source review](references/risk-source-review.md) <br>
- [Change log](references/change-log.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON-backed local reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local routing records, usage statistics, skill indexes, overlap reports, and inbox state when the bundled maintenance scripts are used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
