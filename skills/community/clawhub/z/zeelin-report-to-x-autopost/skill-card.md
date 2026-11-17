## Description:

Automatically selects the latest unposted report from a configured report website or JSON feed, drafts an English X/Twitter post, publishes through the user's logged-in X web session, and records posted reports to avoid duplicates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate recurring promotion of report updates to X while avoiding duplicate posts. It is suited for daily or weekly report-sharing workflows that rely on a logged-in browser session and local posting-history state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public posts to the X account already logged in on the machine, including through recurring cron runs.

Mitigation: Confirm the active X session and review generated post text before enabling unattended schedules.

Risk: Posting is delegated to an external tweet.sh script outside this skill's artifact.

Mitigation: Inspect and approve the referenced posting script before installation, and verify it posts only to the intended account.

Risk: Local posting-history state controls duplicate prevention and can affect whether reports are skipped or reposted.

Mitigation: Protect the state file location and verify its contents before scheduled production use or recovery.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/kelcey2023/skills/zeelin-report-to-x-autopost)
- [THU-ZeeLin Reports source site](https://thu-nmrc.github.io/THU-ZeeLin-Reports/)
- [X web publishing target](https://x.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration steps, and generated social-post text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local posting-history state and cron scheduling guidance when requested.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
