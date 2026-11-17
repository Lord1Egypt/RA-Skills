## Description:

Monitor award availability via the Seats.aero API across configurable watchers, emit unconfirmed alerts for availability transitions, and persist idempotent watcher state in SQLite or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softtrymee](https://clawhub.ai/user/softtrymee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and travel automation agents use this skill to monitor Seats.aero award availability for configured routes, cabins, programs, seat counts, and date windows. It returns candidate alert events for downstream notification or manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Seats.aero API key could be exposed if an authenticated request is redirected off-site.

Mitigation: Use a scoped API key where possible and fix or restrict redirect handling before production use.

Risk: The skill persists watcher configuration and state to local SQLite or JSON files.

Mitigation: Use trusted state and configuration paths, apply normal file permissions, and back up watcher configuration before using replacement options.

Risk: Alerts are candidate signals from Seats.aero and are not airline-confirmed.

Mitigation: Manually confirm availability with the airline or booking program before transferring points or booking travel.

## Reference(s):

- [Seats.aero Partner API](https://seats.aero/partnerapi)
- [Seats.aero](https://seats.aero/)
- [ClawHub Skill Page](https://clawhub.ai/softtrymee/skills/seats-aero-monitor)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration]

**Output Format:** [JSON summaries with alert event payloads and human-readable alert messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Seats.aero API key and local watcher state in SQLite or JSON.]

## Skill Version(s):

3.98.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
