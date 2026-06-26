## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engahmedsalah358-lgtm](https://clawhub.ai/user/engahmedsalah358-lgtm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to send user-approved WhatsApp messages to third parties and to sync or search WhatsApp chat history through the wacli CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a real WhatsApp account through QR login and the external wacli CLI. <br>
Mitigation: Install only when the user trusts wacli and is comfortable linking the account. <br>
Risk: A message or attachment could be sent to the wrong recipient if the request is ambiguous. <br>
Mitigation: Verify the exact recipient, message text, and attachment path before any send action. <br>
Risk: Synced or searched chat history may persist locally in the default wacli store or a selected store directory. <br>
Mitigation: Limit chat and date scope where possible and account for local persistence in ~/.wacli or the chosen --store directory. <br>


## Reference(s): <br>
- [wacli homepage](https://wacli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/engahmedsalah358-lgtm/whats) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the external wacli CLI after recipient, message, and attachment details are explicit and confirmed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
