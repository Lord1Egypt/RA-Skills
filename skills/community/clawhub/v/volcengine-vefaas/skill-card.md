## Description: <br>
Deploy and manage serverless applications on Volcengine veFaaS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and use the vefaas CLI, deploy web applications and MCP services to Volcengine veFaaS, manage functions, configure environment variables, inspect projects, and troubleshoot authentication, build, and deployment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage non-interactive cloud changes that deploy or update Volcengine resources before the target app, region, or gateway is confirmed. <br>
Mitigation: Review proposed commands before execution, confirm the app, region, and gateway, and remove --yes unless the target deployment is intentional. <br>
Risk: Credential values, environment variables, and debug logs may expose secrets or sensitive deployment details. <br>
Mitigation: Prefer SSO or secret-managed credentials, avoid pasting AK/SK values into chat or shell history, and redact debug logs and environment values before sharing them. <br>


## Reference(s): <br>
- [Authentication Reference](references/authentication.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Environment Variables Reference](references/environment-variables.md) <br>
- [Framework Detection Reference](references/framework-detection.md) <br>
- [MCP Deployment](references/mcp-deployment.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>
- [Template Quickstart](references/cookbooks/template-quickstart.md) <br>
- [Deploy Existing Code](references/cookbooks/deploy-existing-code.md) <br>
- [Manage Functions](references/cookbooks/manage-functions.md) <br>
- [Volcengine Console](https://console.volcengine.com) <br>
- [Volcengine API Gateway Console](https://console.volcengine.com/veapig) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment commands, CLI checks, environment variable guidance, and troubleshooting steps for Volcengine veFaaS workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
