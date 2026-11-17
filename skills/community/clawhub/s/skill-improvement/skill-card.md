## Description:

Helps agents optimize existing Claude skills by diagnosing quality issues, presenting findings, applying selected fixes, and verifying improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acautomata](https://clawhub.ai/user/acautomata)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to audit and improve Claude skills through a diagnose, report, select, execute, and verify workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to review and modify skill files, so incorrect recommendations or edits could affect future skill behavior.

Mitigation: Review selected changes and diffs before applying them, and use disposable test files or a sandbox when verification may execute scripts from another skill.

## Reference(s):

- [Diagnostic Checklist](references/diagnostic-checklist.md)
- [Quality Standards](references/quality-standards.md)
- [Report Templates](references/report-templates.md)
- [Verification Guide](references/verification-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, checklists, proposed file edits, diffs, and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply skill-file changes when the user selects fixes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
