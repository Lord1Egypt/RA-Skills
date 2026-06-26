## Description: <br>
Tracks OpenClaw skill usage, scores calls by duration and complexity weight, and reports daily, weekly, monthly, yearly, and all-time leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to record skill invocations, review leaderboards and error history, and generate daily snapshots or workflow review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists local skill usage and error history under ~/.skill_scoreboard, which may include sensitive information if users record secrets in error messages. <br>
Mitigation: Avoid passing secrets in error messages, review stored records before sharing, and protect or clear ~/.skill_scoreboard according to local data handling requirements. <br>
Risk: The gateway-log parser can read local OpenClaw gateway logs from /tmp/openclaw and persist inferred skill usage. <br>
Mitigation: Run parse_gateway_logs.py only when local log scanning is intended and the operator is comfortable with the log contents being summarized into the scoreboard. <br>
Risk: Cron automation can repeatedly create snapshots and workflow reviews without interactive confirmation. <br>
Mitigation: Enable scheduled runs only after reviewing the scripts and confirming the storage path, timezone, and retention expectations. <br>


## Reference(s): <br>
- [ClawHub Skill Scoreboard release page](https://clawhub.ai/luis1213899/skill-scoreboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands; CLI scripts emit text tables and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists scores, call logs, error logs, daily snapshots, and workflow review JSON under ~/.skill_scoreboard.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
