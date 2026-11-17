## Description:

Send bots to Zoom, Google Meet, and Microsoft Teams meetings. Get live transcripts, recordings, and reports. Works with Vexa Cloud or your own self-hosted instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmitriyg228](https://clawhub.ai/user/dmitriyg228)

### License/Terms of Use:


## Use Case:

Developers and meeting operators use this skill to send Vexa bots to meetings, retrieve transcripts and recordings, create meeting reports, and configure Vexa Cloud or self-hosted Vexa workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional webhook flow can let an external meeting-finished event wake the agent, fetch transcripts, write reports, and update persistent entity memory.

Mitigation: Enable webhooks only on trusted public endpoints and manually review transcript-derived report and memory changes.

Risk: A custom VEXA_BASE_URL can route meeting data and API-key authenticated requests to a nonstandard service.

Mitigation: Use Vexa Cloud or a self-hosted Vexa endpoint you control, and avoid untrusted custom base URLs.

Risk: Meeting and recording deletion commands can remove transcripts, anonymize finalized meetings, or delete recording data.

Mitigation: Require an explicit user request for the exact meeting or recording and use the built-in --confirm DELETE guard.

Risk: Vexa API keys grant access to meeting automation and transcript data.

Mitigation: Have users set credentials themselves through environment variables or local secret files, and never ask them to paste keys into chat.

## Reference(s):

- [Vexa onboarding flow](artifact/references/onboarding-flow.md)
- [Vexa API reference notes](artifact/references/user-api-guide-notes.md)
- [Vexa webhook setup](artifact/references/webhook-setup.md)
- [Vexa API key dashboard](https://vexa.ai/dashboard/api-keys)
- [ClawHub skill page](https://clawhub.ai/dmitriyg228/skills/vexa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON CLI responses, shell commands, and concise chat guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write meeting reports under memory/meetings and can persist Vexa endpoint or credential configuration when the user explicitly sets it up.]

## Skill Version(s):

0.1.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
