## Description: <br>
Update Advisor helps agents check for OpenClaw updates, analyze changelog and risk, and execute confirmed updates with a pre-update recovery watchdog on macOS or Linux systemd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzyling](https://clawhub.ai/user/lzyling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to check whether OpenClaw is up to date, review changelog risk, and perform an explicitly confirmed update with recovery safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Execute mode can modify OpenClaw and briefly register a user-level recovery job. <br>
Mitigation: Use Check mode for read-only review, and run Execute mode only after explicit confirmation plus target version, dry-run, ownership, and watchdog gates. <br>
Risk: Temporary recovery cleanup depends on paths from a local watchdog state file. <br>
Mitigation: Before Execute mode, confirm the printed watchdog state file and job name; after recovery, verify cleanup removes the temporary job and files. <br>


## Reference(s): <br>
- [Update Advisor on ClawHub](https://clawhub.ai/lzyling/update-advisor) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes version comparison, changelog risk assessment, doctor status, rollback preview commands, and explicit confirmation gates for update execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
