## Description: <br>
Use when optimizing existing Claude skills, checking skill quality, auditing skill compliance, or when skills have obvious issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ACautomata](https://clawhub.ai/user/ACautomata) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to diagnose quality and compliance issues in Claude skills, select improvements, apply edits, and verify that the optimized skill still works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-directed edits can introduce incorrect or misleading guidance into a target skill. <br>
Mitigation: Review the diagnostic report and proposed diffs before accepting changes, and keep backups for important skills. <br>
Risk: Verification steps may run target-skill scripts or share sensitive skill content with subagents. <br>
Mitigation: Review verification steps before execution and avoid sharing sensitive skill content unless the target environment permits it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ACautomata/skill-improvement) <br>
- [Diagnostic Checklist](references/diagnostic-checklist.md) <br>
- [Quality Standards](references/quality-standards.md) <br>
- [Report Templates](references/report-templates.md) <br>
- [Verification Guide](references/verification-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, checklists, diffs, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce user-directed file edits and verification reports when applied to a target skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
