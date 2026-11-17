## Description:

A personal Wellness hub for OpenClaw that helps users connect health and wellness sources, normalize daily data, and generate daily or weekly summaries, insights, and reminders inside OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect personal wellness apps, wearables, and phone health aggregators, then produce unified wellness digests for OpenClaw chat channels. It supports official personal authorization and phone OS health aggregator flows rather than credential capture or scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health and wellness data through local files, public tunnel exposure, and chat-channel summaries.

Mitigation: Treat bridge tokens as passwords, expose the bridge only as long as needed, keep its state directory off shared or broadly synced storage, and send digests only to private channels after reviewing their contents.

Risk: The hub can install and orchestrate third-party source skills for individual wellness services.

Mitigation: Review and scan each source skill before installing it, especially before granting OAuth access or API tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/wellness)
- [Wellness source catalog](references/catalog.md)
- [Wellness normalized schema](references/schema.md)
- [Digest templates](references/digest-templates.md)
- [Wellness Bridge](references/bridge.md)
- [Tier 2 ingest protocol](references/ingest-protocol.md)
- [iOS exporter via Shortcuts](references/exporter-ios-shortcuts.md)
- [Android exporter via automation](references/exporter-android-automation.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text guidance with shell commands, plus optional JSON wellness documents and message-tool templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local digest files, channel-formatted summaries, and a sendable message template.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
