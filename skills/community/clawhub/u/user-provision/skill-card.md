## Description: <br>
User Provision helps agents create Office 365 operated by 21Vianet and Adobe Creative Cloud user accounts in single-user or batch workflows, including license assignment, password reset, and notification emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT administrators and support agents use this skill to collect onboarding details, run the office365-tools CLI, create or inspect Office 365 and Adobe accounts, assign products, and summarize provisioning results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad live administrative power for Office 365 and Adobe account creation, password reset, licensing, and bulk actions. <br>
Mitigation: Install only in a controlled admin environment, use least-privilege dedicated credentials, and require explicit confirmation before create, reset, or bulk operations. <br>
Risk: Initial passwords and OAuth or API credentials could be exposed in chat summaries, logs, or copied environment files. <br>
Mitigation: Do not echo initial passwords in chat or logs, keep credentials in approved secret handling paths, and send credentials only through an approved secure channel. <br>
Risk: The workflow depends on an external office365-tools repository whose behavior may change outside the skill artifact. <br>
Mitigation: Pin and review the external repository before use, and treat its README, CLAUDE.md, docs, and CLI signatures as the source for execution details. <br>


## Reference(s): <br>
- [office365-tools repository](https://github.com/eggyrooch-blip/office365-tools) <br>
- [User Provision ClawHub page](https://clawhub.ai/eggyrooch-blip/user-provision) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, environment templates, and account-provisioning summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve sensitive account identifiers and initial-password handling; credentials should be delivered only through approved secure channels.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
