## Description: <br>
A personal Wellness hub for OpenClaw that helps users connect health and wellness sources, normalize data, and generate daily or weekly digests, insights, and reminders inside chat channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect personal wellness apps, wearables, and phone health aggregators to OpenClaw, then produce unified daily or weekly wellness summaries for chat channels. It supports official personal authorization and a phone-side bridge for Apple Health or Android Health Connect data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive health and wellness data from wearables, apps, Apple Health, or Android Health Connect. <br>
Mitigation: Use only with data the user chooses to sync, keep tokens and exported files local where possible, and avoid posting digests to shared channels unless the destination is confirmed. <br>
Risk: The Tier 2 bridge may expose a local ingest endpoint through a public tunnel. <br>
Mitigation: Keep the tunnel URL and bearer token private, stop the tunnel when syncing is complete, rotate the token if exposed, and review the bridge before using it with real health data. <br>
Risk: Bridge payloads may remain stored after syncing. <br>
Mitigation: Periodically delete stored bridge payloads that are no longer needed and restrict access to the local bridge state directory. <br>
Risk: Generated wellness digests may omit fields, combine sparse sources, or be interpreted as medical guidance. <br>
Mitigation: Treat summaries as personal tracking aids, review source coverage and missing fields, and do not use the skill for diagnosis, treatment, or medical decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gavinchengcool/wellness) <br>
- [Publisher profile](https://clawhub.ai/user/gavinchengcool) <br>
- [Source catalog](artifact/references/catalog.md) <br>
- [Wellness normalized schema](artifact/references/schema.md) <br>
- [Wellness Bridge](artifact/references/bridge.md) <br>
- [Tier 2 ingest protocol](artifact/references/ingest-protocol.md) <br>
- [iOS exporter](artifact/references/exporter-ios-shortcuts.md) <br>
- [Android exporter](artifact/references/exporter-android-automation.md) <br>
- [Digest templates](artifact/references/digest-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, generated digest text, and optional message-tool template JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read normalized wellness source files, store bridge payloads locally, and prepare channel-specific wellness digest messages.] <br>

## Skill Version(s): <br>
0.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
