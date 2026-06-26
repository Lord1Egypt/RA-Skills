## Description: <br>
轻量化大学生个人效率管家，帮助学生管理课表、查询空教室、生成复习计划、安排运动计划并汇总今日日程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students use this skill to turn course schedules, exam dates, study needs, and exercise preferences into concise daily plans that avoid class-time conflicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores course times, locations, exams, study plans, and exercise plans in local files under memory/student. <br>
Mitigation: Avoid entering sensitive information, restrict local filesystem access, and clear the stored files when the planner is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/student-assistant) <br>
- [Planning Algorithms Reference](references/planning-algorithms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Concise Markdown with schedule summaries and JSON-backed planning data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single responses are intended to stay under 20 lines; generated plans may be persisted under memory/student.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
