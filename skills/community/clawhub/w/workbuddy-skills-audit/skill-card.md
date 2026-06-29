## Description: <br>
Audit installed WorkBuddy skills to identify duplicates, platform-mismatched skills, and maintenance candidates, then generate a structured cleanup report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderszhan](https://clawhub.ai/user/anderszhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit installed WorkBuddy skills, compare them with an approved golden list, and identify unknown or platform-specific skills for manual review before cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup guidance can lead to removal of useful skills if the audit classifications are followed without review. <br>
Mitigation: Review the generated report and confirm any cleanup or deletion actions before removing skill directories. <br>
Risk: Broad activation wording may cause the skill to run during general skill-maintenance conversations. <br>
Mitigation: Use it when explicitly auditing or tidying installed skills, and treat its report as decision support rather than automatic cleanup. <br>


## Reference(s): <br>
- [Golden List - Authorized Skills Reference](artifact/references/golden-list.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderszhan/workbuddy-skills-audit) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown audit report with summary tables and cleanup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a dated skills-audit report and may include review or removal recommendations that require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
