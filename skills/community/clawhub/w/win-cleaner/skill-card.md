## Description:

Deep clean Windows C drive junk files by analyzing disk usage, identifying safe-to-delete items, and cleaning caches, temp files, logs, browser data, application caches, Windows Store, .NET, game, and video-conferencing caches while protecting user data and system stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ftois](https://clawhub.ai/user/ftois)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support-focused agents use this skill to assess and reclaim space on Windows C drives by scanning disk usage, proposing cleanup steps, and running PowerShell cleanup commands for caches, logs, update data, and other re-creatable junk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically delete important app or user state and weaken recovery options despite presenting cleanup steps as safe.

Mitigation: Review every command before execution, start with scan/report behavior, and skip high-impact steps unless the user explicitly accepts the tradeoff.

Risk: DISM resetbase and VSS resizing can reduce the ability to uninstall updates or recover from system changes.

Mitigation: Prefer quick-clean phases when recovery options matter, and run DISM resetbase or VSS resizing only after explicit user confirmation.

Risk: Browser, IDE, and Teams cleanup can remove sessions, history, workspace metadata, databases, or local storage.

Mitigation: Close affected apps, back up important state, and skip browser history or cookies, IDE workspaceStorage, Teams databases, and Teams local storage unless reviewed.

Risk: Desktop and profile-wide heuristic deletions can match files the user may still need.

Mitigation: Treat Desktop and profile-wide findings as review-only candidates and require explicit item selection before deletion.

## Reference(s):

- [Win Cleaner ClawHub page](https://clawhub.ai/ftois/skills/win-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline PowerShell code blocks and cleanup summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scan results, proposed cleanup actions, confirmation prompts, and per-phase freed-space totals.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
