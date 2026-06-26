## Description: <br>
Track parcels via the 17TRACK API (local SQLite DB, polling + optional webhook ingestion). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
ClawHub users and agents use this skill to track parcel status through 17TRACK, manage local parcel records, and summarize delivery changes such as delivery, exceptions, customs holds, and carrier handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 17TRACK API token for API-backed tracking actions. <br>
Mitigation: Configure TRACK17_TOKEN as a secret and avoid echoing or logging it in agent responses. <br>
Risk: Parcel tracking history is stored in the workspace-local data directory. <br>
Mitigation: Keep the workspace and TRACK17_DATA_DIR access-controlled before adding sensitive shipment details. <br>
Risk: Webhook ingestion can accept malformed or spoofed payloads if exposed without trusted controls. <br>
Mitigation: Prefer polling unless webhooks are needed; when using webhooks, keep the receiver behind a trusted endpoint and configure TRACK17_WEBHOOK_SECRET. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tristanmanchester/track17) <br>
- [17TRACK Tracking API v2.2 endpoint](https://api.17track.net/track/v2.2) <br>
- [17TRACK carrier metadata endpoint](https://res.17track.net/asset/carrier/info/apicarrier.all.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRACK17_TOKEN for API-backed actions; webhook use is optional.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
