## Description: <br>
WorkTracker helps AI assistant teams keep a local record of work starts, progress updates, completions, status reports, logs, backups, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isenlink](https://clawhub.ai/user/isenlink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent team operators use this skill to track assistant work activity, progress, completion notes, and team status in local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Work logs, backups, and exports may contain sensitive operational details and are treated as plaintext. <br>
Mitigation: Avoid recording secrets, credentials, customer data, incident details, or other sensitive content; restrict local file access and retention. <br>
Risk: The documentation claims security controls that the evidence says are not verifiably implemented. <br>
Mitigation: Do not rely on encryption, access control, or audit-log claims until the publisher provides verifiable implementation evidence. <br>
Risk: The skill persistently stores work activity on the local system. <br>
Mitigation: Install only where persistent local work tracking is intended, and review log, backup, and export locations before operational use. <br>


## Reference(s): <br>
- [WorkTracker ClawHub release](https://clawhub.ai/isenlink/work-tracker) <br>
- [README](artifact/README.md) <br>
- [WorkTracker training manual](artifact/docs/WorkTracker培训手册.md) <br>
- [Basic usage example](artifact/examples/basic_usage.sh) <br>
- [Team collaboration example](artifact/examples/team_collaboration.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown and terminal text with local JSON, CSV, and Markdown file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes persistent plaintext work logs, status files, backups, and exports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
