## Description: <br>
Helps OpenClaw users inspect disk usage and clean old backup, temporary, Vim swap, and session files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mickey3721](https://clawhub.ai/user/mickey3721) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and maintainers use this skill to review local OpenClaw storage, identify cleanup candidates, and run guided maintenance for backups, temporary files, session files, and gateway status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental deletion of local OpenClaw backup or temporary files. <br>
Mitigation: Run the cleanup manually first, inspect the listed files, and approve deletion only after confirming they are no longer needed. <br>
Risk: Deleting Vim swap files can prevent recovery of unsaved edits. <br>
Mitigation: Check for active editing sessions and recover or close files before allowing swap-file cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mickey3721/system-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and maintenance guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local files that should be reviewed before deletion.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
