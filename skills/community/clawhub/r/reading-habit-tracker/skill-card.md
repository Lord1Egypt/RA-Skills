## Description:

閱讀習慣追蹤系統：目標設定（年目標/書單/頁數/時長）、進度追蹤、每週/每月分析報告、落後預警、視覺化統計。與 reading_progress.py（專注打卡）差異化：目標導向、計劃管理、深度數據分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage reading goals, maintain booklists, log reading sessions, review weekly or monthly progress, and receive lagging-progress alerts in Traditional Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reading goals, reading sessions, booklists, and reports in a local user directory.

Mitigation: Install only on systems where local reading history and notes can be stored under ~/.bookshelf-plus/habit_tracker.

Risk: Delete and remove commands can change or remove locally stored reading-goal, session, or booklist data.

Mitigation: Review delete and remove commands before running them, and keep backups of the habit-tracker directory when the data matters.

Risk: The suggested cron job can create recurring reading-progress alerts.

Mitigation: Add the cron job only when recurring alerts are wanted, and review its schedule, timezone, and message before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuan905/skills/reading-habit-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/xuan905)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from local reading goals, session logs, and booklist data stored under ~/.bookshelf-plus/habit_tracker.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
