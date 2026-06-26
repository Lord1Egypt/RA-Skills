## Description: <br>
Phone number formatting, cache inspection, contact export, and message ID generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run WhatsApp automation utilities that format or clean phone numbers, inspect OpenClaw WhatsApp cache information, export cached contacts, and generate WhatsApp-style message IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local OpenClaw WhatsApp state and display cached contacts in the conversation or logs. <br>
Mitigation: Run contact export only on explicit user request, avoid shared or untrusted agent sessions, and review outputs before storing or sharing them. <br>
Risk: Cache inspection can reveal local WhatsApp state paths and session metadata. <br>
Mitigation: Use cache inspection only when troubleshooting a trusted local setup and avoid pasting resulting paths or metadata into public channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarcosRippel/whatsapp-utils) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text] <br>
**Output Format:** [JSON emitted by Node.js command-line utilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read local OpenClaw WhatsApp state when inspecting cache information or exporting contacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
