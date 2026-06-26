## Description: <br>
个人健身跟踪器 — 通过文字记录健身训练数据，自动解析动作、组数、次数和重量，实时写入本地 MySQL 数据库。支持制定专属训练计划、查询历史记录、追踪进步曲线，以及球类和有氧运动记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[query1988](https://clawhub.ai/user/query1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal fitness agents use this skill to record strength, cardio, and sport workouts in a local MySQL database, query training history, and generate training plans from prior activity and available equipment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workout records are saved to a local MySQL database configured by the user. <br>
Mitigation: Use a dedicated local database and least-privilege database user for normal tracking. <br>
Risk: MYSQL_PASSWORD is required for database access and could be exposed through shell history, committed files, or overly broad file permissions. <br>
Mitigation: Keep MYSQL_PASSWORD out of version control, prefer a private environment file or interactive entry, and restrict file permissions. <br>
Risk: Database setup may require privileges beyond normal runtime tracking. <br>
Mitigation: Run setup only with privileges needed to create tables, then use minimal INSERT, SELECT, UPDATE, and DELETE permissions for routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/query1988/workout-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/query1988) <br>
- [README](artifact/README.md) <br>
- [Local configuration and tools](artifact/TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local MySQL configuration through MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, and MYSQL_SOCKET.] <br>

## Skill Version(s): <br>
1.3.7 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
