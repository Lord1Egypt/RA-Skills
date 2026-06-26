## Description: <br>
Session Manager tracks conversation sessions, prompts before starting new topics, and records sessions to a user-selected Feishu Bitable or local Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zh40](https://clawhub.ai/user/zh40) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to keep long agent conversations organized by detecting topic changes, opening new sessions with consent, and saving summaries, decisions, and follow-up items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session records can retain sensitive conversation details in local Markdown files or a configured Feishu workspace. <br>
Mitigation: Choose the storage destination deliberately and avoid saving sensitive details unless that storage location is appropriate for the user's needs. <br>
Risk: Automatic topic-shift detection may suggest a new session at the wrong time. <br>
Mitigation: Ask the user to confirm before opening a new session and before carrying previous context forward. <br>


## Reference(s): <br>
- [Session template](references/session-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/zh40/session-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Conversation prompts plus Markdown session records or Feishu Bitable field entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md with current session state and save records in the user-selected storage location.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
