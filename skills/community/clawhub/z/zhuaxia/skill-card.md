## Description: <br>
Zhuaxia exports and imports OpenClaw instances as portable .claw packages for backup, sharing, migration, and restoration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lovelcp](https://clawhub.ai/user/Lovelcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Zhuaxia to back up, transfer, import, or roll back OpenClaw workspace and configuration state, including bundled skills, while reviewing credentials and installation effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: .claw imports can install active skills, overwrite workspace files, and introduce imported configuration. <br>
Mitigation: Run a dry-run first, review bundled skills, overwritten files, required credentials, and imported configuration before loading. <br>
Risk: Rollback may not fully remove all changes from an import. <br>
Mitigation: Keep the generated backup ID and manually check for new workspace files, installed skills, and imported configuration that should be removed. <br>
Risk: .claw files or URLs can alter an OpenClaw instance. <br>
Mitigation: Treat .claw packages like installable software and load only packages from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lovelcp/zhuaxia) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node; produces and loads .claw package files through the bundled CLI.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
