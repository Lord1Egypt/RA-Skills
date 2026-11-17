## Description:

Student timetable manager for self or parent-managed child profiles. Includes init flow + profile registry under schedules/profiles/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:


## Use Case:

Students, parents, and guardians use this skill to initialize, store, query, and migrate local timetable data for one or more student profiles. Agents can answer today, tomorrow, this-week, and next-week schedule questions, manage wake keywords, and add special events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or incorrect schedule profile data could lead the skill to return misleading timetable information.

Mitigation: Use the skill only in workspaces where schedules/profiles data and the profile registry are trusted, and confirm profile identity when ambiguity is reported.

Risk: Student or child school metadata is stored in local JSON files.

Mitigation: Avoid entering unnecessary sensitive information and restrict workspace access to users who should see the timetable data.

Risk: Legacy migrations may change local schedule files if overwrite or backup behavior is not acceptable for the workspace.

Mitigation: Run migration dry-runs first, review planned changes, and verify backups before applying migrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extraterrest/skills/student-timetable)
- [Publisher profile](https://clawhub.ai/user/extraterrest)
- [README](artifact/README.md)
- [StudentTimetable Schema v2](artifact/schema_v2.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON files, guidance]

**Output Format:** [Plain text schedule responses, CLI output, and JSON schedule/profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local schedules/profiles data; profile ambiguity returns clarification instead of selecting a profile.]

## Skill Version(s):

0.1.0-alpha.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
