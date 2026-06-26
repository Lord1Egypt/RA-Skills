## Description: <br>
Study Buddy helps parents of middle- and high-school students plan study routines, record check-ins, track progress, manage wrong-question notes, and generate local study reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External parents and guardians use this skill to organize a child's study plan, record daily learning activity, monitor progress, manage wrong-question review, and produce study summaries. It is a study-management aid and does not provide subject teaching or replace educational decisions by parents, teachers, or tutors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child-related study records are stored locally and may be visible to other users on a shared computer. <br>
Mitigation: Use a private account or set STUDY_BUDDY_HOME to an isolated directory, then delete the data directory when the records are no longer needed. <br>
Risk: Study plans and feedback may be treated as authoritative educational advice. <br>
Mitigation: Use the output as planning support and review it against the child's school requirements, parent judgment, and qualified educator guidance. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/study-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text guidance with shell command examples; the CLI can write local JSON study records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local storage under ~/.study-buddy by default and supports STUDY_BUDDY_HOME for an isolated data directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence, SKILL.md frontmatter, clawhub.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
