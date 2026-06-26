## Description: <br>
A cognitive protocol for safely managing and auditing OpenClaw application upgrades by analyzing configuration-level risks, runtime behavior shifts, and changelog signals before changes are applied. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RadonX](https://clawhub.ai/user/RadonX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to assess OpenClaw upgrades, identify configuration and runtime risks, plan mitigations, and verify behavior before and after an upgrade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Upgrade analysis may recommend configuration changes or production-impacting verification tests. <br>
Mitigation: Confirm the target workspace and deployment, review proposed changes, and require operator approval before applying config changes or running impactful tests. <br>
Risk: Generated audit and verification reports may capture sensitive operational details. <br>
Mitigation: Keep reports free of secrets and review artifacts before sharing or committing them. <br>
Risk: Manual cleanup or monitoring commands may affect local files or logs if run without review. <br>
Mitigation: Preview command targets and backup or preserve relevant artifacts before deletion or cleanup. <br>


## Reference(s): <br>
- [Changelog Analysis Patterns](references/changelog_analysis_patterns.md) <br>
- [Risk Categories](references/RISK_CATEGORIES.md) <br>
- [Audit Report Template](references/AUDIT_REPORT_TEMPLATE.md) <br>
- [Verification Checklist](references/VERIFICATION_CHECKLIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with checklists, verification steps, and inline shell commands or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workspace-relative upgrade reports and verification notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
