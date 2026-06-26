## Description: <br>
学分查询技能用于按学生姓名和科目查询本地学生成绩记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bc96](https://clawhub.ai/user/bc96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, or support agents can use this skill to answer single-subject or all-subject score queries from a local sample score database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student score data may be sensitive if the bundled records are not sample data or if users are not authorized to view them. <br>
Mitigation: Deploy only with sample data or authorized records, and verify access expectations before exposing query results. <br>
Risk: Raw grade queries are written to console output, which may be retained in shared logs. <br>
Mitigation: Avoid logging identifiable score queries in shared environments, or remove query logging before deployment. <br>
Risk: The metadata declares an ffmpeg binary requirement even though the skill behavior is a local score lookup. <br>
Mitigation: Review and remove the unused binary requirement so installers do not grant or install unnecessary runtime capability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bc96/score-query) <br>
- [Publisher profile](https://clawhub.ai/user/bc96) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain-language Chinese response with structured result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success or error status, a human-readable message, and score data when a match is found.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
