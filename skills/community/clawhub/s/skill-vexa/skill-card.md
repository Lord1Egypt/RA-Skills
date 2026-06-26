## Description: <br>
Send bots to Zoom, Google Meet, and Microsoft Teams meetings; get live transcripts, recordings, and reports; and use self-hosted or cloud Vexa endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DmitriyG228](https://clawhub.ai/user/DmitriyG228) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Vexa meeting bots, capture transcripts and recordings, configure webhooks, and create meeting reports from Google Meet, Microsoft Teams, or Zoom sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled API-key files may expose usable Vexa credentials or encourage unsafe secret handling. <br>
Mitigation: Remove the bundled secrets directory before installation, rotate any exposed keys, and configure a fresh VEXA_API_KEY through the user's preferred secret-management path. <br>
Risk: Webhook-driven actions can trigger report creation and file writes when external meeting events are received. <br>
Mitigation: Review webhook mappings before use, require an authenticated public hook endpoint, and validate which meeting reports and memory files the agent may create or modify. <br>
Risk: Meeting transcripts, recordings, share links, and download URLs may contain sensitive participant or business information. <br>
Mitigation: Confirm user intent before retrieving, sharing, downloading, deleting, or storing meeting data, and prefer least-retention workflows for reports and recordings. <br>
Risk: Destructive meeting or recording deletion commands can purge transcripts, anonymize data, or delete recording assets. <br>
Mitigation: Require an explicit user request for the exact meeting or recording and use the command's confirmation guard before any destructive action. <br>


## Reference(s): <br>
- [ClawHub Skill Vexa page](https://clawhub.ai/DmitriyG228/skill-vexa) <br>
- [Vexa onboarding flow](references/onboarding-flow.md) <br>
- [Vexa API reference notes](references/user-api-guide-notes.md) <br>
- [Vexa webhook setup](references/webhook-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Conversational guidance, shell commands, JSON command output, and Markdown meeting reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local meeting report files and Vexa configuration files when invoked by an agent.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
