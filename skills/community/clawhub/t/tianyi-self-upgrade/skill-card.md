## Description:

Self-Upgrade helps OpenClaw maintain and upgrade itself through version checks, configuration migration, dependency checks, repair workflows, backups, rollback guidance, and upgrade reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fffdz](https://clawhub.ai/user/fffdz)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw maintainers use this skill to check OpenClaw versions, migrate deprecated configuration fields, inspect required skills and packages, run repair commands, and produce an upgrade report with backup and validation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change OpenClaw authentication configuration with weak user controls.

Mitigation: Use dry-run or manually supervised execution, review the exact configuration diff before auth migration, and require explicit authorization before changing API keys or tokens.

Risk: Automatic repair or migration may alter OpenClaw configuration in ways that are hard to undo.

Mitigation: Create an independent backup of ~/.openclaw/openclaw.json before execution and verify the documented rollback path is implemented before relying on it.

Risk: Rollback guidance may not match the implemented command surface.

Mitigation: Do not rely on the documented -RollbackTo command unless it has been verified in the installed script; restore from a known backup manually when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fffdz/skills/tianyi-self-upgrade)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown upgrade report with PowerShell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup paths, validation results, changed configuration fields, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
