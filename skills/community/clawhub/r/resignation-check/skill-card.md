## Description: <br>
Checks Office 365 and Adobe tenant users against Feishu contact records by email, reports likely departed accounts, and can delete confirmed candidates after explicit user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT operations and identity administrators use this skill to compare Office 365 and Adobe account inventories with Feishu directory records, classify likely offboarded users, and generate deletion reports. The skill is intended for controlled account cleanup workflows that require manual confirmation before deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can delete Microsoft 365 and Adobe accounts. <br>
Mitigation: Run a report-only pass first, manually verify every candidate, and require explicit per-account approval before deletion. <br>
Risk: The workflow depends on unpinned external office365-tools code. <br>
Mitigation: Review and pin the external repository before installation or execution. <br>
Risk: The workflow requires sensitive Microsoft 365, Adobe, Feishu, and SMTP credentials. <br>
Mitigation: Use least-privilege dedicated credentials and keep secrets out of reports, logs, and prompts. <br>
Risk: Notification email may be sent during account cleanup. <br>
Mitigation: Disable notification email unless the operator explicitly needs and approves it. <br>


## Reference(s): <br>
- [ClawHub Resignation Check release page](https://clawhub.ai/eggyrooch-blip/resignation-check) <br>
- [office365-tools project repository](https://github.com/eggyrooch-blip/office365-tools) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Adobe User Management API base](https://usermanagement.adobe.io/v2/usermanagement) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write timestamped resignation reports and per-provider deletion logs under /tmp when executed by an agent.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
