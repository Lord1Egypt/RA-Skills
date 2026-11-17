## Description:

Load per-job runtime instructions from Google Sheets, cache them locally, and reconcile cron job enablement flags safely for OpenClaw operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage OpenClaw job runtime instructions and cron enablement from a Google Sheet control plane without manually editing local job configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Google Sheet can persistently steer job runtime instructions.

Mitigation: Treat the sheet as an operational authority, restrict access tightly, and periodically inspect or clear cached runtime-instruction files.

Risk: Cron reconciliation can bulk-change job enabled flags and missing rows can disable jobs.

Mitigation: Run dry-run first, review the planned changes, and apply only after confirming the sheet fully represents intended job state.

Risk: Service-account credentials are required for sheet access.

Mitigation: Use least-privilege read-only credentials and store private keys in a secret manager.

## Reference(s):

- [Google Sheet Runtime Instructions Schema](references/google-sheet-instructions-schema.md)
- [ClawHub skill page](https://clawhub.ai/danielsinewe/skills/runtime-instructions-control-plane)
- [Publisher profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated local JSON and Markdown runtime-instruction files when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Google Sheets credentials or cached local runtime-instruction files.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
