## Description: <br>
Provides QQ Mail summaries and reminders for visible mailbox metadata, label unread counts, and public share-page content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal mailbox operators use this skill to summarize visible QQ Mail list metadata, unread label counts, and public share links without automating login, sending, receiving, or permission bypass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox metadata can include private information such as subjects, senders, folders, timestamps, and unread status. <br>
Mitigation: Only ask the agent to inspect folders, labels, and share links you are comfortable exposing; do not provide QQ credentials directly to the agent. <br>
Risk: Using the skill beyond its documented scope could create unsafe account interactions such as login automation, sending, receiving, or bypass attempts. <br>
Mitigation: Use normal QQ Mail login flows and keep the agent limited to visible summary, unread-count, and public share-page tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/qq-mail) <br>
- [QQ Mail homepage](https://mail.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes visible metadata and public share-page information only; no executable code or persistence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
