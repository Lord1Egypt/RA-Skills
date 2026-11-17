## Description:

Migrates the WorkBuddy data directory from the Windows system drive to a fixed non-system drive using a directory junction so data, runtimes, logs, and caches stay off C:.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guibe7391](https://clawhub.ai/user/guibe7391)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and support agents use this skill when a Windows system drive is low on space and WorkBuddy data, caches, or bundled runtimes need to be relocated to a non-system disk while preserving the original C: path through a junction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A failed or misdirected migration could cause WorkBuddy data loss.

Mitigation: Back up the full WorkBuddy directory before use, close WorkBuddy completely, and verify the copied database, projects, sessions, skills, and junction before deleting any old data.

Risk: The automatic destination selection could place the WorkBuddy profile on an unintended non-system drive.

Mitigation: Confirm the target drive and workbuddy-data path before running the bundled migration script, especially on machines with multiple fixed disks.

Risk: The scripts can move and delete profile data and may leave old data behind if files are locked.

Mitigation: Run only after manual review, keep the migration log, and remove any remaining .workbuddy_old folder only after confirming WorkBuddy opens correctly and the junction points to the intended destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guibe7391/skills/workbuddy-data-migration)
- [Lessons learned](references/lessons.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bundled Windows batch and Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration instructions and local script execution steps for Windows WorkBuddy installations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
