## Description: <br>
Book real estate showing tours from emailed or pasted listing details, including extracting listing data, preparing outbound call jobs, coordinating a calling sub-agent, creating calendar invites, and returning confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Real estate agents, brokerage staff, and assistants use this skill to turn emailed or pasted listing requests into showing call queues, blocked-item reports, confirmation summaries, and calendar invite files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can share client, listing, scheduling, and contact details during outbound showing calls without clear consent boundaries. <br>
Mitigation: Use the skill only where the user has explicitly approved outbound calls and share the minimum necessary details with the calling workflow. <br>
Risk: A showing could be reported as confirmed before the booking result actually confirms the slot. <br>
Mitigation: Do not mark a showing as confirmed until the call result explicitly includes a confirmed date and time. <br>
Risk: Outbound real estate calls may be subject to local consent, caller identification, and telemarketing requirements. <br>
Mitigation: Identify the caller as an AI assistant acting for the brokerage or realtor, respect applicable local requirements, and keep an audit trail of request payloads, call outcomes, and timestamps. <br>


## Reference(s): <br>
- [Email Intake Template](references/email-intake-template.md) <br>
- [Integration Notes](references/integration-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, calendar files, guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands, JSON planning files, and .ics calendar files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live outbound calls should run only after explicit approval; confirmed slots are required before invite files are generated.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
