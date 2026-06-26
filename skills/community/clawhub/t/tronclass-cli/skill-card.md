## Description: <br>
Interact with the TronClass learning management system via the `tronclass` CLI to check courses, assignments, deadlines, grades, announcements, and course materials; download lecture slides or PDFs; and submit homework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujun-bo2](https://clawhub.ai/user/yujun-bo2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Students and external TronClass users use this skill to let an agent run `tronclass` CLI workflows for course lookup, deadline checks, file downloads, announcement review, and homework submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse a saved TronClass login session for broad school-related requests. <br>
Mitigation: Install only when the agent should access the user's TronClass account, use explicit prompts, and run `tronclass auth logout` when session reuse is no longer wanted. <br>
Risk: The skill can perform account-changing actions such as homework submission. <br>
Mitigation: Prefer draft-and-review workflows before final submission and confirm every homework action before execution. <br>
Risk: The skill can download course or announcement files to local paths. <br>
Mitigation: Confirm each download path before running download commands. <br>


## Reference(s): <br>
- [TronClass CLI Skill Page](https://clawhub.ai/yujun-bo2/tronclass-cli) <br>
- [Skill Homepage](https://github.com/YuJun-BO2/tronclass-cli-skill) <br>
- [CLI Tool Homepage](https://github.com/YuJun-BO2/tronclass-cli-ts) <br>
- [TronClass](https://tronclass.com/) <br>
- [Auth Command Reference](references/auth.md) <br>
- [Courses Command Reference](references/courses.md) <br>
- [Activities Command Reference](references/activities.md) <br>
- [Homework Command Reference](references/homework.md) <br>
- [Announcements Command Reference](references/announcements.md) <br>
- [Todo Command Reference](references/todo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that access a saved TronClass session, download files, or submit homework through the local `tronclass` CLI.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
