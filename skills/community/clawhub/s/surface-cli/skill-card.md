## Description: <br>
Use the Surface mail CLI to read and act on Gmail, Outlook, and generic IMAP/SMTP mail through one JSON-first contract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalj99](https://clawhub.ai/user/vishalj99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and engineers use this skill to let an agent inspect, search, triage, draft, send, and manage Gmail, Outlook, or generic IMAP/SMTP mail through Surface CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables agents to access sensitive mailbox contents through a local mail CLI. <br>
Mitigation: Install and configure it only when agent mailbox access is intended, and review account auth status and local Surface configuration before use. <br>
Risk: Mail send, reply, archive, mark-read, and mark-unread actions can mutate a user's mailbox. <br>
Mitigation: Respect Surface write-safety settings, prefer draft workflows for compose tasks, and use configured safe recipients for live-send testing. <br>
Risk: Mailbox passwords, provider tokens, or email content can be exposed through chat, shell history, repository files, or external summarization. <br>
Mitigation: Avoid pasting mailbox passwords into chat or repos, prefer password environment/file/command mechanisms, and confirm the user accepts any external summarizer privacy tradeoff before enabling it. <br>


## Reference(s): <br>
- [Surface CLI homepage](https://github.com/VishalJ99/surface-cli) <br>
- [ClawHub skill page](https://clawhub.ai/vishalj99/surface-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to parse Surface CLI JSON output and use stable message and thread refs.] <br>

## Skill Version(s): <br>
0.4.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
