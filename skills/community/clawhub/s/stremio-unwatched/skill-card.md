## Description:

Check a Stremio library for unwatched TV episodes, view upcoming release calendars, sync a dedicated Google Calendar, and download new episodes through Stremio or supported torrent clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patfitzner](https://clawhub.ai/user/patfitzner)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect a Stremio account's TV library, identify aired but unwatched episodes, generate upcoming episode calendars, and initiate downloads or calendar syncs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Download commands can start Stremio or torrent downloads without the advertised dry-run or confirmation.

Mitigation: Run download commands with --dry-run or --magnets first, and avoid no-argument stremio_download.sh until the default behavior is fixed.

Risk: The skill can access a Stremio account, local credential cache, installed Stremio addons, local Stremio clients, and torrent clients.

Mitigation: Use it only in a trusted environment, protect ~/.openclaw/credentials/stremio.json, and run stremio_auth.sh --logout when access should be removed.

Risk: Authentication commands can print Stremio auth keys for piping.

Mitigation: Treat printed auth keys as secrets and avoid exposing terminal logs or command output that may contain them.

Risk: Calendar commands can create or delete events in the dedicated Stremio TV Google Calendar.

Mitigation: Review the dedicated calendar before mutation, limit sync windows with --days, and use --gcal-clear only when deletion is intended.

## Reference(s):

- [Stremio API Reference](artifact/references/stremio_api.md)
- [ClawHub Skill Page](https://clawhub.ai/patfitzner/skills/stremio-unwatched)
- [Stremio](https://www.stremio.com)
- [gog CLI](https://gogcli.sh)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands; scripts can emit terminal tables or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may access local credentials, Stremio APIs, installed addons, torrent clients, and a dedicated Google Calendar when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
