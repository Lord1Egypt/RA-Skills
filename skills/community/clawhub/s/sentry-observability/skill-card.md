## Description: <br>
Adds observability to an OpenClaw instance by sending errors, logs, and traces to Sentry, then supports investigation with the Sentry plugin and `sentry` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergical](https://clawhub.ai/user/sergical) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Sentry observability for OpenClaw and investigate errors, traces, structured logs, events, and issues through the Sentry CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry can include sensitive logs, traces, personal data, or operational details sent to Sentry. <br>
Mitigation: Use a dedicated Sentry project, scrub secrets and personal data before forwarding telemetry, and lower trace sampling or disable log forwarding when full capture is not appropriate. <br>
Risk: Sentry CLI and API examples include commands that create, update, resolve, assign, or delete resources. <br>
Mitigation: Use least-privilege Sentry tokens and require explicit confirmation before running mutation-capable commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sergical/sentry-observability) <br>
- [Sentry CLI command reference](references/cli-commands.md) <br>
- [OpenClaw Sentry plugin implementation guide](references/plugin-setup.md) <br>
- [Sentry CLI docs](https://cli.sentry.dev) <br>
- [Sentry API docs](https://docs.sentry.io/api/) <br>
- [Sentry Node SDK docs](https://docs.sentry.io/platforms/javascript/guides/node/) <br>
- [OpenClaw Sentry plugin source](https://github.com/sergical/openclaw-plugin-sentry) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash, JSON, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Sentry CLI binary and Sentry credentials for commands that access or modify Sentry resources.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
