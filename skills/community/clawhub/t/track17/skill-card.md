## Description:

Track parcels via the 17TRACK API with a local SQLite database, polling, and optional webhook ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to let an agent register, list, poll, and summarize parcel tracking status through 17TRACK while storing package data locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a 17TRACK API token and sends tracking numbers plus carrier parameters to 17TRACK.

Mitigation: Install only when that token use and data sharing are acceptable, and never echo TRACK17_TOKEN in agent responses or logs.

Risk: Optional webhook handling may accept forged updates according to the server security summary.

Mitigation: Prefer polling with sync, or avoid public webhook exposure until the signature-enforcement issue is fixed.

Risk: Parcel labels may be sent to 17TRACK as tags without making that behavior clear.

Mitigation: Use non-sensitive labels or set an explicit non-sensitive tag when adding packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/track17)
- [17TRACK API v2.2 endpoint](https://api.17track.net/track/v2.2)
- [17TRACK carrier metadata resource](https://res.17track.net/asset/carrier/info/apicarrier.all.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a 17TRACK API token and stores parcel data in a workspace-local SQLite database.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
