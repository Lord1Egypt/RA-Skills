## Description:

Social Media Scheduler helps agents schedule and publish text, media, threads, and bulk content calendars across Discord, Reddit, Twitter/X, Mastodon, Bluesky, Moltbook, LinkedIn, and Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrshorrid](https://clawhub.ai/user/mrshorrid)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to plan, queue, publish, and monitor social posts across multiple platforms from a CLI-oriented workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard and queue storage can expose or misuse social-media credentials and scheduled posts.

Mitigation: Review before installing, run the dashboard only on trusted local machines, and use low-scope platform credentials.

Risk: Tokens or full credential values may be retained in storage/queue.json.

Mitigation: Rotate any tokens that may have been stored there and store credential references instead of full secrets.

Risk: The dashboard lacks enough protection for shared or exposed environments.

Mitigation: Bind only to loopback, add authentication, restrict CORS, and avoid browsing untrusted sites while the dashboard is running.

Risk: Configuration values and dependencies need hardening before broad deployment.

Mitigation: Redact configuration data from API responses and update vulnerable dependencies before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrshorrid/skills/social-scheduler)
- [README](README.md)
- [Complete Usage Guide](SKILL.md)
- [Media Upload Guide](MEDIA-GUIDE.md)
- [Social Platform API Research](API-RESEARCH.md)
- [Moltbook API](https://github.com/moltbook/api)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Discord Developer Documentation](https://discord.com/developers/docs)
- [Mastodon API Documentation](https://docs.joinmastodon.org/api/)
- [AT Protocol Documentation](https://atproto.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and CLI workflow descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill's tooling can create local queue and analytics JSON files when used.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
