## Description: <br>
Generate Vercel API commands for deployment management, including deployment status, build logs, domain SSL checks, recent deployments, rollback, and environment-variable audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to generate reviewable Vercel API commands for checking deployment status, viewing logs, inspecting domains, listing deployments, promoting rollbacks, auditing environment-variable metadata, and seeing deployment setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commands require a Vercel token and may expose credentials if copied into shared chats, terminals, or logs. <br>
Mitigation: Use the least-privileged token available, replace placeholders locally, and avoid sharing token-bearing commands or environment output. <br>
Risk: Rollback commands promote a deployment to production and can change live site behavior. <br>
Mitigation: Review the project name and deployment ID before running a rollback command, and treat rollback as a live production change. <br>
Risk: Environment-variable auditing can reveal sensitive project configuration metadata. <br>
Mitigation: Review command output locally and avoid pasting environment-variable details into shared chats or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/vercel-tool) <br>
- [Vercel API](https://api.vercel.com) <br>
- [Vercel account tokens](https://vercel.com/account/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands use placeholder credentials and are intended for user review before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
