## Description:

WorkTracker helps AI assistant teams record starts, progress updates, completions, status reports, and local work logs for traceable team coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isenlink](https://clawhub.ai/user/isenlink)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI assistant team operators use this skill to track local work status, progress updates, completion notes, and team activity reports across one or more assistants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local work logs and exports may contain confidential project, staffing, customer, or operational information.

Mitigation: Review before installing in sensitive workspaces, keep the WorkTracker directory private, and avoid exporting records to shared locations.

Risk: The artifact advertises encryption, role permissions, audit logging, restore, repair, and cleanup controls that the security evidence says should not be relied on unless the implementation is updated.

Mitigation: Treat those controls as unverified and use external access controls and backups until the implementation is reviewed and updated.

Risk: Default documentation suggests broad filesystem permissions for records and backups.

Mitigation: Use private permissions such as 700 for the WorkTracker directory and 600 for records and backups.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/isenlink/skills/work-tracker)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [WorkTracker training manual](artifact/docs/WorkTracker培训手册.md)
- [Basic usage example](artifact/examples/basic_usage.sh)
- [Team collaboration example](artifact/examples/team_collaboration.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Plain text and Markdown status/log output, with optional JSON or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local JSON and Markdown records under the user's workspace and can export status data.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
