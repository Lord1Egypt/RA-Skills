## Description: <br>
Create a pre-restart audit and rollback archive for system-level changes where failed restarts would be painful to diagnose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zczcm85](https://clawhub.ai/user/zczcm85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill before restart-sensitive system changes to preserve before-state backups, execution plans, diffs, verification notes, and rollback paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archived system configuration backups may contain sensitive data. <br>
Mitigation: Only pass files to --copy-before when they are intentionally being archived, and store the archive in a secure, persistent location. <br>
Risk: A local workspace fallback archive may not survive the failure scenario it is meant to support. <br>
Mitigation: Prefer an explicit archive root, SYSTEM_CHANGE_ARCHIVE_ROOT, or a writable persistent storage candidate before using fallback storage. <br>


## Reference(s): <br>
- [System Change Archive on ClawHub](https://clawhub.ai/zczcm85/system-change-archive) <br>
- [Archive Schema](references/archive-schema.md) <br>
- [Path Resolution Rules](references/path-resolution.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured PRE-RESTART and POST-RESTART archive records for audit, verification, and rollback.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
