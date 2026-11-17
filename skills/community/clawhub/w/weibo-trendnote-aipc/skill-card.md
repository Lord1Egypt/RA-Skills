## Description:

Fetches Weibo realtime hot search rankings, summarizes trending topics with a local model, and appends the hot list plus digest to an Obsidian note on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinquan251](https://clawhub.ai/user/yinquan251)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers use this skill to capture current Weibo hot-search trends, create a local summary, and save the resulting digest into an Obsidian note. It supports one-time runs and user-requested recurring automation on Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local state and appends generated content to an Obsidian note.

Mitigation: Run a one-time execution first and verify the configured vault, note path, and generated digest before enabling recurring use.

Risk: Environment overrides can change which local programs are executed for summarization, note writing, or OpenClaw cron management.

Mitigation: Review env.ps1 and any SUMMARIZE_BIN, NOTESMD_BIN, or OPENCLAW_BIN values before running the skill.

Risk: Optional recurring automation can create background runs every 5 and 10 minutes.

Mitigation: Use install-crons only when ongoing automation is intended, and review or remove the registered OpenClaw cron jobs when no longer needed.

## Reference(s):

- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)
- [ClawHub skill page](https://clawhub.ai/yinquan251/skills/weibo-trendnote-aipc)

## Skill Output:

**Output Type(s):** [shell commands, markdown, text, configuration]

**Output Format:** [Markdown digest, console text, and local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Windows-local state and can append generated digest content to an Obsidian note; recurring OpenClaw cron jobs are optional.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
