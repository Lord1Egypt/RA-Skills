## Description: <br>
Track skill execution details including matched skills, decomposed tasks, execution status, outputs, and timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abo-hub](https://clawhub.ai/user/Abo-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep an append-only audit trail of skill matches, task decomposition, execution status, outputs, timestamps, and generated artifacts across conversation turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad per-turn audit logging can retain prompts, replies, outputs, and file paths locally. <br>
Mitigation: Install only where this logging is intentional, and define retention, deletion, and redaction rules before use. <br>
Risk: The skill performs PM2/.env inspection and a public-IP network check to locate a Deck URL. <br>
Mitigation: Review whether the deployment environment permits that system and network discovery before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abo-hub/skill-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/Abo-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSONL records and short text reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Append-only local tracking records may include prompts, replies, outputs, timestamps, statuses, and artifact paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
