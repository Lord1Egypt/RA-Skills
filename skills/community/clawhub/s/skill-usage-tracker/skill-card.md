## Description: <br>
Automatically tracks and audits skill usage, enforces rules from SKILL_USAGE_RULES.md, logs violations, and generates daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SASAMITTRRR](https://clawhub.ai/user/SASAMITTRRR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor whether required skill-usage rules are followed, record violations, and produce daily audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs and daily reports may capture sensitive conversation or compliance details. <br>
Mitigation: Confirm what is written to skill_violations.log and daily reports, avoid use where sensitive conversations could be logged without consent, and delete or rotate logs when they are no longer needed. <br>
Risk: Rule-checking results depend on the contents and currency of SKILL_USAGE_RULES.md. <br>
Mitigation: Review the rules file before relying on the audit output and update it as usage policies change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SASAMITTRRR/skill-usage-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown instructions with local log and daily report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write skill_violations.log and daily reports when its audit workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
