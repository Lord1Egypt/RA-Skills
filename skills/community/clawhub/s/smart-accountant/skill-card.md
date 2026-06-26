## Description: <br>
Provides expert double-entry accounting support including GST compliance, audit controls, period closing, journal entries, and financial reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dakshhmehta](https://clawhub.ai/user/dakshhmehta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business owners, accountants, and agent developers use this skill to draft, validate, post, rectify, close, and report on double-entry accounting records with GST-aware checks. It is intended for local accounting workflows that require human confirmation before financial records are changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly change sensitive accounting records through local database scripts. <br>
Mitigation: Use a test or backed-up database first and require explicit human approval before posting, reversing, rectifying, closing periods, migrating schema, or running maintenance. <br>
Risk: Raw or improvised SQL workflows could bypass the intended accounting controls. <br>
Mitigation: Disable or avoid raw SQL workflows and prefer the documented scripts with Maker-Checker review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dakshhmehta/smart-accountant) <br>
- [Accountant Agent Skill Mastery Guide](artifact/SKILL.md) <br>
- [Audit Control Rulebook](artifact/audit_rule.md) <br>
- [GST Guard Skill](artifact/gst_guard.md) <br>
- [Database Tooling Guide](artifact/db_tool.md) <br>
- [Tool Package Manifest](artifact/tool/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JavaScript/SQLite tool usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces accounting workflows, GST checks, journal previews, database operations, report instructions, and local tool commands; financial mutations require human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
