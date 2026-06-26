## Description: <br>
Send bots to Zoom, Google Meet, and Microsoft Teams meetings. Get live transcripts, recordings, and reports. Works with Vexa Cloud or your own self-hosted instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DmitriyG228](https://clawhub.ai/user/DmitriyG228) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and meeting operators use this skill to send Vexa bots to Google Meet, Microsoft Teams, and Zoom meetings, retrieve transcripts and recordings, configure optional webhooks, and generate local meeting reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Vexa meeting data, transcripts, recordings, bot controls, and local report storage. <br>
Mitigation: Install only in workspaces where that access is acceptable, keep API keys private, and avoid custom endpoints or share/download links unless the destination is trusted. <br>
Risk: Optional webhook automation can turn external meeting-finished events into agent tasks that write persistent local memory and entity notes. <br>
Mitigation: Keep the webhook disabled unless automatic reports are needed; if enabled, restrict the public hook endpoint, verify hook authentication, and review memory/entity changes before relying on them. <br>
Risk: Meeting and recording deletion commands can remove or anonymize Vexa data. <br>
Mitigation: Run destructive commands only after an explicit user request for the exact meeting or recording and require the documented confirmation flag. <br>


## Reference(s): <br>
- [ClawHub Skill Vexa listing](https://clawhub.ai/DmitriyG228/vexa) <br>
- [Vexa onboarding flow](references/onboarding-flow.md) <br>
- [Vexa API reference notes](references/user-api-guide-notes.md) <br>
- [Vexa webhook setup](references/webhook-setup.md) <br>
- [Vexa API keys dashboard](https://vexa.ai/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and generated local Markdown meeting reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can call Vexa APIs and write meeting reports under memory/meetings when the user runs report workflows.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
