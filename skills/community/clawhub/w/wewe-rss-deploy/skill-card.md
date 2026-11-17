## Description:

Deploys WeWe RSS to fetch WeChat public-account articles through WeChat Reading and generate RSS feeds with SQLite configuration and optional background process management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agasding](https://clawhub.ai/user/agasding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, configure, run, verify, and uninstall a local WeWe RSS service that exposes RSS and API feeds for WeChat public-account articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs upstream project code without pinning a known commit.

Mitigation: Pin the upstream repository or archive to a reviewed commit, verify downloads, and review dependency changes before running install or build commands.

Risk: The deployment example binds the service to 0.0.0.0 on port 4000.

Mitigation: Bind to localhost unless network exposure is required, restrict access with firewall or reverse-proxy controls, and use a strong auth code.

Risk: The configuration uses a default third-party WeChat Reading relay URL.

Mitigation: Use that relay only if trusted, or replace it with a self-hosted or reviewed relay endpoint.

Risk: PM2 startup can make the service persist across restarts.

Mitigation: Enable PM2 startup only after explicit approval and document how to stop and remove the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agasding/skills/wewe-rss-deploy)
- [ClawHub publisher profile](https://clawhub.ai/user/agasding)
- [WeWe RSS upstream project](https://github.com/cooderl/wewe-rss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, env, and table snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, environment configuration, API endpoint examples, troubleshooting, and uninstall guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
