## Description: <br>
Checks a Stremio library for unwatched TV episodes, shows upcoming release dates, downloads new episodes through Stremio or supported torrent clients, and can sync upcoming episodes to Google Calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PatFitzner](https://clawhub.ai/user/PatFitzner) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect a Stremio TV library, identify aired episodes that are not watched, review upcoming episode calendars, and start or preview downloads. It is also useful for agents that need shell-command workflows around Stremio authentication, library queries, calendar sync, and download status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a Stremio auth token or credentials through shared shells, logs, or local credential files. <br>
Mitigation: Treat the Stremio auth key as a secret, avoid exposing credentials in shared shells or logs, and clear cached credentials when they are no longer needed. <br>
Risk: Download commands can start real torrent downloads through Stremio or supported torrent clients. <br>
Mitigation: Use --dry-run, --filter, and --limit before download commands, and review the selected episodes before starting downloads. <br>
Risk: The Google Calendar clear flow can delete events from the dedicated Stremio TV calendar. <br>
Mitigation: Run --gcal-clear only when intentionally removing events from the dedicated Stremio TV calendar. <br>


## Reference(s): <br>
- [Stremio API Reference](references/stremio_api.md) <br>
- [Stremio](https://www.stremio.com) <br>
- [Stremio Central API](https://api.strem.io/api) <br>
- [gog CLI](https://gogcli.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/PatFitzner/stremio-unwatched) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and node or bun; optional flows use gog and supported torrent clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
