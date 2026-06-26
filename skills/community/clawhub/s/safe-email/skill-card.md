## Description: <br>
Safe Email processes explicitly forwarded messages from a dedicated IMAP inbox, extracts structured details, and returns safe next-step suggestions without automatically reading or acting on external systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitansde](https://clawhub.ai/user/nitansde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to process a newly forwarded email in a dedicated inbox, extract structured details such as sender, subject, dates, locations, links, and action items, and decide on follow-up steps while keeping mailbox access explicit and minimal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox access through IMAP can expose messages in the dedicated inbox. <br>
Mitigation: Use a dedicated inbox and app password, forward only emails intended for processing, and run the skill only after explicit user instruction. <br>
Risk: Deletion or permanent expunge could remove the wrong message if approved ambiguously. <br>
Mitigation: Confirm the exact message before deletion and require explicit consent before moving it to Trash or expunging it. <br>
Risk: Email details such as time windows, links, or action items may be incomplete or ambiguous. <br>
Mitigation: Return confidence notes and clarification questions instead of taking downstream action automatically. <br>


## Reference(s): <br>
- [Safe Email on ClawHub](https://clawhub.ai/nitansde/safe-email) <br>
- [Publisher profile: nitansde](https://clawhub.ai/user/nitansde) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown structured summary with suggested next actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extraction-only; no automatic downstream writes; optional email deletion requires explicit consent.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
