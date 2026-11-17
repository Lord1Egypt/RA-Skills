## Description:

Tracks albums, podcasts, shows, films, and YouTube channels in local Markdown files so an agent can log culture, find past favorites, and answer questions about what the user has watched or listened to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a private, searchable culture journal for media that shaped their thinking, including albums, podcasts, shows, films, and YouTube channels. The agent can create or update Markdown records, search saved entries, surface taste patterns, and connect shared cultural references with people when companion skills are installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and update guidance includes unpinned remote fetches or package installation paths.

Mitigation: Prefer a pinned release or commit and verify the downloaded SKILL.md before installation or update.

Risk: Heartbeat or cron reminder guidance can create recurring agent checks over personal media notes.

Mitigation: Enable HEARTBEAT.md or cron reminders only when the user explicitly wants recurring checks.

Risk: The skill stores personal cultural preferences and notes in local Markdown files.

Mitigation: Keep the mind/vibes folder in a trusted workspace and review entries before sharing or syncing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilyabelikin/skills/vibes-skill)
- [Haah skill](https://github.com/haah-ing/haah-skill)
- [Peeps skill](https://github.com/haah-ing/peeps-skill)
- [Pages skill](https://github.com/haah-ing/pages-skill)
- [Nooks skill](https://github.com/haah-ing/nooks-skill)
- [Digs skill](https://github.com/haah-ing/digs-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown records and concise natural-language guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and searches local files under mind/vibes when the user chooses to use the skill.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
