## Description:

每周一 09:00 自动处理周例会 Excel 跟进表，更新日期列，并将结果发送到指定美信工作群。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff or developers use this skill to automate a recurring weekly meeting workflow: find the latest scoped Excel follow-up sheet, create the current-week version, update the date column, and share it to the configured Meixin work group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs scheduled file creation or modification under D:\00OPENCLAWSPACE\.

Mitigation: Confirm the target directory, filename pattern, and Monday 09:00 Asia/Shanghai schedule before enabling the cron task.

Risk: The skill sends the generated Excel file to a configured Meixin group.

Mitigation: Confirm the group ID, account permissions, and file sensitivity before allowing outbound sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/weekly-meeting-automation)
- [Publisher profile](https://clawhub.ai/user/paudyyin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text with command snippets and cron configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces status-oriented agent guidance for a Windows Excel and Meixin group-send workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
