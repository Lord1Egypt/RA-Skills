## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafay0313](https://clawhub.ai/user/rafay0313) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they explicitly want an agent to send WhatsApp messages to a third party, transfer a file, or search and sync WhatsApp history through wacli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WhatsApp messages or files to other people through an authenticated wacli session. <br>
Mitigation: Require an explicit recipient and message or file, ask clarifying questions when ambiguous, and confirm the exact recipient and content before sending. <br>
Risk: The local wacli store may contain WhatsApp session or chat data. <br>
Mitigation: Authenticate only on trusted machines and treat ~/.wacli, or any configured alternate store, as sensitive. <br>
Risk: History backfill results depend on the user's phone being online and are best-effort. <br>
Mitigation: Tell users when backfill may be incomplete and avoid presenting sync or search results as exhaustive. <br>


## Reference(s): <br>
- [wacli homepage](https://wacli.sh) <br>
- [wacli Go module](https://github.com/steipete/wacli) <br>
- [ClawHub skill page](https://clawhub.ai/rafay0313/tt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external wacli CLI and an authenticated WhatsApp session on a trusted machine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
