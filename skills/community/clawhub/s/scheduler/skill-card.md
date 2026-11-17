## Description:

Scheduler helps agents use a local command-line productivity logger for scheduling, planning, tracking, reminders, review, search, status checks, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when an agent needs to manage local scheduling and productivity notes through a shell-based scheduler command. It supports adding, planning, tracking, reviewing, searching, and exporting locally stored scheduler entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduler and productivity text is stored locally under ~/.local/share/scheduler and can be exported on request.

Mitigation: Avoid entering secrets or highly sensitive personal information, and review exported files before sharing them.

Risk: CSV exports may be opened in spreadsheet software before export escaping is hardened.

Mitigation: Inspect CSV exports before opening them in spreadsheet tools, especially when entries may begin with formula-like characters.

Risk: Local file permissions are not described as hardened in the security guidance.

Mitigation: Use the skill only in trusted local environments and restrict access to the scheduler data directory as needed.

## Reference(s):

- [Scheduler Skill Page](https://clawhub.ai/ckchzh/skills/scheduler)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Configuration]

**Output Format:** [Markdown or plain text with shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and read local log and export files under ~/.local/share/scheduler.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
