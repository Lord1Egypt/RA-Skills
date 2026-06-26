## Description: <br>
Read, search, and manage Zoho Mail via the Zoho Mail REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ragsagar](https://clawhub.ai/user/ragsagar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through authenticated Zoho Mail REST API workflows, including account discovery, folder listing, message reading, search, threads, labels, attachments, and regional endpoint selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized mailbox access through OAuth credentials. <br>
Mitigation: Install only for Zoho accounts the operator is authorized to access and use the narrow read-only scopes shown in the skill. <br>
Risk: Exposure of sensitive email content while reading or searching messages. <br>
Mitigation: Avoid printing full message bodies unless needed and review command output before sharing logs or transcripts. <br>
Risk: Client secrets or refresh tokens could be leaked through shell history, logs, or shared chats. <br>
Mitigation: Keep Zoho OAuth secrets in environment variables, avoid pasting them into shared contexts, and revoke or rotate refresh tokens when access is no longer needed. <br>


## Reference(s): <br>
- [Zoho Mail API documentation](https://www.zoho.com/mail/help/api/) <br>
- [Zoho API Console](https://api-console.zoho.com/) <br>
- [ClawHub skill page](https://clawhub.ai/ragsagar/zoho-mail-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and jq JSON projections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and Zoho OAuth environment variables before API calls can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
