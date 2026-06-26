## Description: <br>
Monitor award availability via the Seats.aero API across configurable route, program, cabin, and date-window watchers, emitting unconfirmed alerts on none-to-available transitions while persisting watcher state in SQLite or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softtrymee](https://clawhub.ai/user/softtrymee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and travel-award automation users use this skill to configure Seats.aero watchers, check cached award availability, and receive JSON alert events for candidate award seats. Alerts are intentionally unconfirmed and should be verified with the airline or booking program before transfer or purchase decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Seats.aero API key. <br>
Mitigation: Provide the key through SEATS_AERO_API_KEY only for trusted runs, and keep it out of committed files, shared logs, and shell history. <br>
Risk: The skill creates and updates local SQLite or JSON watcher state, including bulk replacement and date-update workflows. <br>
Mitigation: Back up state before using --replace-watchers or broad date updates, and use --dry-run before applying bulk changes. <br>
Risk: Seats.aero alerts are candidate signals and may be stale or inaccurate. <br>
Mitigation: Treat alert events as unconfirmed and verify availability with the airline or booking program before transferring points or purchasing travel. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/softtrymee/seats-aero-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/softtrymee) <br>
- [Seats.aero](https://seats.aero/) <br>
- [Seats.aero partner API endpoint](https://seats.aero/partnerapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runner emits JSON summaries and alert_events; watcher state is persisted locally in SQLite or JSON.] <br>

## Skill Version(s): <br>
3.98.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
