## Description: <br>
Read and send emails using the SolEmail automation system when asked to check emails, send files via email, respond to an email, or set up email automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read a local email store, summarize or inspect messages, send SMTP email, attach files, and configure scheduled email checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose personal mailbox content to an agent. <br>
Mitigation: Install only for mailboxes the user intends the agent to access, and limit scheduled checks to read-only workflows unless sending is explicitly approved. <br>
Risk: The skill can send messages and attachments through a configured SMTP account. <br>
Mitigation: Use an app-specific password and review recipients, subject lines, message bodies, and attachment lists before outbound email is sent. <br>
Risk: The file-search-and-zip workflow can package local files into outbound attachments. <br>
Mitigation: Use narrow search directories and avoid broad folders such as home, Documents, Downloads, or locations that may contain secrets. <br>


## Reference(s): <br>
- [SolEmail guide](https://thesolai.github.io/guides/email-automation/) <br>
- [SolEmail repository](https://github.com/TheSolAI/SolEmail) <br>
- [SolEmail technical report](https://github.com/TheSolAI/SolEmail/blob/main/report.md) <br>
- [himalaya email client](https://github.com/soywod/himalaya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and script-driven text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read mailbox content, send outbound messages, and package local files as email attachments when configured with local mail and SMTP credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
