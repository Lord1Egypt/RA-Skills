## Description:

Monitor topics of interest and proactively alert when important developments occur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and external users use this skill to configure scheduled monitoring for product releases, news, research, competitor updates, and other topics, then receive high-priority alerts or weekly digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feed discovery, RSS/Atom feeds, GitHub release feeds, and OPML imports can cause the skill to access unrestricted user-supplied URLs.

Mitigation: Use only trusted public HTTPS feed and discovery URLs, and avoid importing OPML files from untrusted sources.

Risk: Alerts and digests may send monitored topic details through Telegram, Discord, email, or another agent-delivered channel.

Mitigation: Do not monitor sensitive internal topics when notification channels could expose the resulting content outside the intended audience.

Risk: The documentation includes an unpinned pip installation path for feedparser even though the release vendors dependencies.

Mitigation: Prefer the bundled vendored dependency or a pinned virtual environment for any external dependency installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/skills/topic-monitor)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [DigitalOcean OpenClaw Skills guide](https://www.digitalocean.com/resources/articles/what-are-openclaw-skills)
- [feedparser project](https://github.com/kurtmckee/feedparser/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and text alert or digest summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit structured alert payloads for agent-delivered Telegram, Discord, or email notifications.]

## Skill Version(s):

1.6.0 (source: frontmatter and changelog, released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
