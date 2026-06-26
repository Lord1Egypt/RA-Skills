## Description: <br>
AI智能出题考试系统 - 基于文档自动生成考试、指派学员并查询结果 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangzidetiandi](https://clawhub.ai/user/xiangzidetiandi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, training teams, and enterprise administrators use this skill to create exams from uploaded documents, assign them to named users or departments, and query individual or batch exam results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload documents, create exams, assign users or departments, and query personal exam results. <br>
Mitigation: Install and run it only with authorization for the connected exam system, the source documents, learner identities, and score data. <br>
Risk: Credentials, access tokens, user identifiers, department names, exam IDs, and scores may appear in configuration or console output. <br>
Mitigation: Use least-privilege credentials, keep secrets out of chats and repositories, and avoid running in environments where logs are broadly visible. <br>
Risk: Assignments by department or name search can target unintended people when names are ambiguous or departments are broad. <br>
Mitigation: Verify the configured API endpoint and confirm exact users and departments before creating or assigning an exam. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiangzidetiandi/soke-ai-exam-skill) <br>
- [Publisher profile](https://clawhub.ai/user/xiangzidetiandi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [JavaScript module responses, console output, and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured application credentials and API endpoint access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
