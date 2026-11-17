## Description:

Helps an agent recover and summarize current or previous OpenClaw session content from local session archive files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to locate session archives, parse JSONL records, and produce a concise session recall report with key points, unfinished tasks, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose archived conversations, hidden thinking fields, partial tool results, credentials, tokens, or sensitive code from local session files.

Mitigation: Use it only on sessions the user owns or is explicitly authorized to inspect, and redact thinking fields, tool results, credentials, tokens, and sensitive code from recovery reports.

Risk: The workflow can parse the wrong private, group, or reset archive if the target session is selected too broadly.

Mitigation: Confirm the target session key or file path before parsing and limit the report to the requested session and necessary excerpts.

## Reference(s):

- [parse_session.py](references/parse_session.py)
- [Session Recover ClawHub page](https://clawhub.ai/axelhu/skills/session-recover)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown session recall report with inline shell commands and extracted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, message excerpts, and summarized session context; should omit credentials, tokens, private thinking, sensitive tool results, and sensitive code.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
