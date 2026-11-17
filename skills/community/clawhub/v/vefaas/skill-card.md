## Description:

Deploy and manage serverless applications on Volcengine veFaaS. Use when the user wants to deploy web apps, agents, skills as APIs, tool pages, webhook functions, manage existing functions (pull code, upload and deploy), configure environment variables, or work with veFaaS services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhn233](https://clawhub.ai/user/songhn233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy web applications, APIs, webhook functions, agents, and existing function code to Volcengine veFaaS. It also guides authentication checks, project inspection, environment variable management, configuration updates, and troubleshooting for veFaaS deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global CLI from a tarball distribution channel.

Mitigation: Install only after trusting the Volcengine distribution channel, and check `vefaas --version` before use or when unsupported behavior appears.

Risk: Noninteractive deployment commands can upload code or modify cloud resources without a separate prompt.

Mitigation: Use least-privilege Volcengine credentials, verify the target app, function, region, gateway, and inspected settings before deploy or push, and reserve `--yes` for controlled workflows.

Risk: Debug logs and imported environment files can expose credentials or service secrets.

Mitigation: Use only the declared VOLC credentials, do not probe unrelated secret stores, and redact tokens, keys, `.env` values, and debug request or response payloads before sharing logs.

Risk: Incorrect framework detection, port selection, or dependency declarations can produce broken deployments.

Mitigation: Run `vefaas inspect` before every deploy, ensure dependencies are declared in `package.json` or `requirements.txt`, and override build, output, command, runtime, or port settings when detection is wrong.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhn233/skills/vefaas)
- [veFaaS CLI tarball distribution](https://vefaas-cli.tos-cn-beijing.volces.com/volcengine-vefaas-latest.tgz)
- [Configuration Reference](references/configuration.md)
- [Framework Detection Reference](references/framework-detection.md)
- [Troubleshooting Reference](references/troubleshooting.md)
- [Template Quickstart](cookbooks/template-quickstart.md)
- [Deploy Existing Code](cookbooks/deploy-existing-code.md)
- [Manage Functions](cookbooks/manage-functions.md)
- [Volcengine API Gateway console](https://console.volcengine.com/veapig)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include deployment, authentication, environment-variable, inspection, troubleshooting, and configuration steps for the veFaaS CLI.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
