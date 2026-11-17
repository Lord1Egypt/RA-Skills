## Description:

Add observability to your OpenClaw instance - errors, logs, and traces sent to Sentry - and investigate issues with the Sentry CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergical](https://clawhub.ai/user/sergical)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure Sentry telemetry for an OpenClaw instance and investigate errors, logs, traces, issues, and events with the Sentry CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Sentry admin/API commands can create, modify, resolve, assign, or delete resources when run with privileged credentials.

Mitigation: Use least-privilege Sentry credentials and require human review for DELETE requests or broad sentry api commands.

Risk: Telemetry forwarding can send secrets or personal data to Sentry if logs and diagnostic events are not scrubbed.

Mitigation: Redact secrets and personal data before forwarding telemetry and review plugin filters before production use.

Risk: Installing or copying third-party plugin code can introduce supply-chain or implementation risk.

Mitigation: Verify or pin plugin code before installation and review the implementation against the documented OpenClaw configuration path.

## Reference(s):

- [Sentry CLI Command Reference](artifact/references/cli-commands.md)
- [OpenClaw Sentry Plugin Implementation Guide](artifact/references/plugin-setup.md)
- [Sentry CLI docs](https://cli.sentry.dev)
- [Sentry API docs](https://docs.sentry.io/api/)
- [Sentry Node SDK docs](https://docs.sentry.io/platforms/javascript/guides/node/)
- [Sentry Structured Logs docs](https://docs.sentry.io/platforms/javascript/guides/node/logs/)
- [Sentry CLI log command docs](https://cli.sentry.dev/commands/log/)
- [OpenClaw Sentry plugin implementation](https://github.com/sergical/openclaw-plugin-sentry)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Sentry CLI and Sentry credentials; some Sentry AI commands require Seer, GitHub integration, and code mappings.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
