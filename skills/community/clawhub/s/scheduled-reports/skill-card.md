## Description: <br>
Define, preview, approve, and manage recurring reports for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xvespertine](https://clawhub.ai/user/0xvespertine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to convert recurring reporting requests into approved OpenClaw report definitions and cron jobs with locked data sources, delivery targets, preview approval, validation, and lifecycle controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring report can deliver incorrect or sensitive information if its schedule, sources, recipients, webhook URL, output folder, or preview are not reviewed before activation. <br>
Mitigation: Review the schedule, locked data sources, delivery target, output location, and preview artifact before enabling; use allowed-domain or approved-target controls where available. <br>
Risk: Report data can contain untrusted content that attempts to influence runtime behavior. <br>
Mitigation: Treat report data as content rather than instructions, and keep queries, exclusions, business rules, delivery targets, and runtime guards locked. <br>
Risk: Saved definitions, previews, and run artifacts can expose confidential reporting data if kept in shared locations. <br>
Mitigation: Store definitions, previews, and run artifacts in private, access-controlled paths and keep them out of normal Git history unless explicitly approved and protected. <br>


## Reference(s): <br>
- [Report Definition](references/REPORT_DEFINITION.md) <br>
- [Scheduled Reports on ClawHub](https://clawhub.ai/0xvespertine/scheduled-reports) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON report definitions and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final scheduled report definitions are expected to validate with scripts/validate_report_definition.py before activation or resume.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
