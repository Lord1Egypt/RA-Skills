## Description:

Search and analyze your own session logs (older/parent conversations) using jq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate, inspect, and summarize prior OpenClaw session transcripts when a user asks about older conversations or missing historical context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad access to historical conversation logs that may include secrets or personal information.

Mitigation: Ask for a specific session, date, or phrase before searching, and avoid returning raw transcript text unless it is necessary and appropriate.

Risk: Historical transcript inspection can expose more context than the user intended to share in the current task.

Mitigation: Limit searches to the requested scope and summarize relevant findings instead of dumping complete conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1yihui/skills/yihui-session-logs)
- [Publisher profile](https://clawhub.ai/user/1yihui)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local session JSONL files and requires jq and ripgrep for the documented command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
