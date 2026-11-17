## Description:

Study Buddy helps parents of middle- and high-school students create study plans, log daily check-ins, track progress, manage wrong-question notes, and generate study reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially parents of middle- and high-school students, use this skill to manage study routines, track learning activity, record wrong questions, and generate local progress reports. It supports learning management and habit building, not subject-matter tutoring or educational decision replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a child's study profile, learning logs, wrong-question entries, and reports as local JSON files.

Mitigation: Use STUDY_BUDDY_HOME to isolate data on shared machines, restrict local file access as appropriate, and delete the data directory when records are no longer needed.

Risk: Generated plans, reports, and feedback are study-management aids and may be incomplete or unsuitable for a student's specific needs.

Mitigation: Have a parent, teacher, or qualified advisor review recommendations before relying on them for important education decisions.

## Reference(s):

- [Study Buddy Command Reference](artifact/references/commands.md)
- [Study Buddy Release Page](https://clawhub.ai/harrylabsj/skills/study-buddy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores profile, plan, log, wrong-question, and report records locally under ~/.study-buddy/ by default, or under STUDY_BUDDY_HOME when configured.]

## Skill Version(s):

1.2.0 (source: frontmatter, skill.json, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
