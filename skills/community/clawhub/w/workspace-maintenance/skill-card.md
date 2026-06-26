## Description: <br>
Maintain workspace documentation hygiene and discoverability by organizing markdown sprawl, updating doc indexes, archiving stale progress/status snapshots, generating dry-run cleanup candidate lists, and keeping memory/task control files aligned without deleting files automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houseofjuici](https://clawhub.ai/user/houseofjuici) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to keep workspace documentation findable, archive stale status material, refresh indexes, and produce reviewable cleanup reports without automatic deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled audit script uses a hard-coded archive path that may not match the user's workspace. <br>
Mitigation: Confirm or adjust the archive path before running the script, and keep the workspace under version control when possible. <br>
Risk: Cleanup candidates or document moves could affect active documentation if reviewed too quickly. <br>
Mitigation: Review dry-run reports and move manifests before taking deletion or cleanup action, and keep active control files in the workspace root. <br>
Risk: Dry-run deletion reports could be mistaken for approval to delete files. <br>
Mitigation: Treat generated deletion candidate lists as review material only; the skill should not delete files automatically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/houseofjuici/workspace-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command steps and generated text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dry-run candidate reports, move manifests, task status updates, and completion summaries for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
