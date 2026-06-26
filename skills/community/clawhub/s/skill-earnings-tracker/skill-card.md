## Description: <br>
Tracks skill marketplace earnings and performance across ClawHub, EvoMap, ReelMind, and custom sources for reporting and portfolio analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KyleChen26](https://clawhub.ai/user/KyleChen26) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill to log marketplace metrics, produce weekly or monthly earnings reports, list tracked skills, and export local earnings records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive earnings, credit balances, customer details, or notes may be written to plaintext local files. <br>
Mitigation: Keep records non-sensitive, avoid secrets and private customer data in notes, and protect or delete ~/.openclaw/earnings as needed. <br>
Risk: Automation examples can persist scheduled logging jobs. <br>
Mitigation: Review the exact cron command before installing it and document how to remove or disable it. <br>


## Reference(s): <br>
- [Skill Earnings Tracker on ClawHub](https://clawhub.ai/KyleChen26/skill-earnings-tracker) <br>
- [ClawHub marketplace](https://clawhub.ai) <br>
- [EvoMap marketplace](https://evomap.ai/marketplace) <br>
- [ReelMind](https://reelmind.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the included CLI writes JSONL earnings records and JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores monthly JSONL records under ~/.openclaw/earnings when the included CLI is run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
