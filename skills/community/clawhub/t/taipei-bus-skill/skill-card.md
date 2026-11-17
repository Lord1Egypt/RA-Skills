## Description:

Provides Taipei bus real-time vehicle lookup, sequence-based ETA estimates, route and stop information, map visualization examples, and anomaly detection using Taipei City and PTX public transit data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Taipei bus questions, inspect live vehicle status, estimate arrival times, search routes and stops, and set up optional monitoring workflows.

### Deployment Geography for Use:

Global, with functionality scoped to Taipei City transit data.

## Known Risks and Mitigations:

Risk: The skill makes public transit API requests and may create local public-data cache files.

Mitigation: Install it only for Taipei bus lookup use cases, keep generated cache files limited to public transit data, and rebuild caches according to the documentation.

Risk: Cron and reminder examples can run background checks and deliver results to configured channels.

Mitigation: Enable scheduled monitoring only as an opt-in workflow and review destination channels before activating notifications.

Risk: The map HTML generator example is not suitable for untrusted input as written.

Mitigation: Serialize marker data safely with JSON.stringify and validate coordinates before using generated map HTML with external or user-supplied data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuan905/skills/taipei-bus-skill)
- [Publisher profile](https://clawhub.ai/user/xuan905)
- [README.zh-TW.md](artifact/README.zh-TW.md)
- [README.en.md](artifact/README.en.md)
- [Documentation README](artifact/docs/README.md)
- [Taipei City bus vehicle data API](https://tcgbusfs.blob.core.windows.net/blobbus/TstBusEvent.json)
- [PTX Taipei bus stop API](https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei)
- [PTX Taipei bus route API](https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei)
- [PTX Taipei stop-of-route API](https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live public transit API results, cached public-data lookups, ETA estimates, route summaries, anomaly reports, or optional cron configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact documentation notes version 1.2.0 content updates)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
