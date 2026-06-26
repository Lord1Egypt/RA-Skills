## Description: <br>
Deploy and manage serverless applications on Volcengine veFaaS, including web apps, APIs, tool pages, webhook functions, existing function updates, environment variables, and veFaaS service configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhn233](https://clawhub.ai/user/songhn233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to deploy and manage Volcengine veFaaS applications and functions, from template initialization through project inspection, environment configuration, deployment, URL discovery, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that create, update, deploy, or push real Volcengine veFaaS cloud resources. <br>
Mitigation: Use least-privilege Volcengine credentials and confirm the target app, function, region, gateway, and code package before running deploy or push commands, especially with --yes. <br>
Risk: The workflow handles access keys, tokens, environment variables, service URLs, and customer data that may appear in debug output or logs. <br>
Mitigation: Redact access keys, tokens, URLs, environment variables, and customer data before sharing logs, and avoid surfacing debug output unless it is needed for troubleshooting. <br>
Risk: The skill requires installing and running the vefaas CLI from the Volcengine distribution tarball. <br>
Mitigation: Install it only when the user intends to manage Volcengine veFaaS resources, then verify the CLI with vefaas --version before using deployment features. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/songhn233/vefaas) <br>
- [vefaas CLI Tarball](https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Framework Detection Reference](references/framework-detection.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>
- [Template Quickstart](cookbooks/template-quickstart.md) <br>
- [Deploy Existing Code](cookbooks/deploy-existing-code.md) <br>
- [Manage Functions](cookbooks/manage-functions.md) <br>
- [Volcengine API Gateway Console](https://console.volcengine.com/veapig) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include veFaaS deployment commands, environment-variable commands, configuration checks, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
