## Description: <br>
Session Recover helps agents reconstruct and summarize current or previous OpenClaw sessions from local JSONL session archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to recover, search, and summarize recent session history after context loss or reset. It is intended for sessions the user owns and can access locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local session archives that can contain private conversations, secrets, internal reasoning, configuration values, and code. <br>
Mitigation: Use it only on sessions you own, confirm the exact file or session key before parsing, and redact sensitive content before sharing any output. <br>
Risk: Recovered context may include more historical conversation content than the user intended to expose. <br>
Mitigation: Prefer narrow tail, keyword, and context options when possible, and review recovered excerpts before including them in summaries or follow-up work. <br>


## Reference(s): <br>
- [parse_session.py](references/parse_session.py) <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/session-recover) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown session recall report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recovered message excerpts, summaries, unfinished tasks, key context, and source file paths or session keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
