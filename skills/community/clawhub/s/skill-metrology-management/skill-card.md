## Description:

Helps metrology administrators and laboratory supervisors maintain instrument ledgers, calculate next calibration dates, flag overdue items, and generate management reports in Markdown with optional Word or Excel exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

External quality, laboratory, and metrology teams use this skill to keep calibration ledgers current, query due or overdue instruments, plan send-out calibration work, and prepare compliance status reports. It supports structured ledger maintenance while leaving certificate conclusions and statutory calibration decisions to authoritative records and procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to run a relative Python report command, but the referenced script is not included in the package.

Mitigation: Review or provide the intended scripts/build_report.py before allowing an agent to execute that command, and inspect generated reports before use.

Risk: Calibration intervals, certificate details, and compliance status can be incomplete or based on defaults when source data is missing.

Mitigation: Verify generated ledger entries against enterprise procedures, current certificates, and statutory calibration requirements before relying on them.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-metrology-management)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-metrology-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports and guidance with optional shell commands for Word or Excel export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report is metrology_report.md; optional exports are metrology_report.docx and metrology_report.xlsx after user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
