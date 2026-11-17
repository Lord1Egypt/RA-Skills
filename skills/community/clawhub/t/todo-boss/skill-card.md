## Description:

Capture and track tasks with owner and due date, mark done, list open or delegated tasks, and get daily reports via Telegram commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ukraecho](https://clawhub.ai/user/ukraecho)

### License/Terms of Use:


## Use Case:

Employees and team leads use this skill in Telegram to capture tasks, assign owners and due dates, track delegated work, and get concise daily remaining-work reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted /todo input can execute local code through task input handling.

Mitigation: Do not install this version where untrusted Telegram users can send /todo messages, and fix the script to pass user text as data rather than Python source before broader deployment.

Risk: Task records are persisted locally in an append-only log.

Mitigation: Define retention and access-control expectations for the local task log before using the skill with sensitive work data.

## Reference(s):

- [Todo Boss ClawHub page](https://clawhub.ai/ukraecho/skills/todo-boss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Short Telegram-ready text responses and local JSONL task events]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates append-only local task records under the user's OpenClaw workspace data directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
