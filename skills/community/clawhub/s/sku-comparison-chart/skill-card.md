## Description:

Turn seller-supplied SKU specs into one SKU comparison chart set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and marketplace operators use this skill to turn confirmed SKU names and seller-supplied spec rows into one comparison still per named axis for listing graphics. The workflow plans the chart list first, then uses Beatra image generation or edit tasks after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a broad shared Beatra device token.

Mitigation: Authorize only when the user accepts the Beatra connection, keep the token in the documented credential file, avoid exposing it in chat, commands, logs, or environment variables, and revoke the device authorization from the Beatra Console when no longer needed.

Risk: The package can silently self-update executable package files.

Mitigation: Review the package before execution, use the documented update controls to disable automatic updates when desired, and rely on the bundled updater's fixed-source, checksum, manifest, rollback, and package-owned-file checks.

Risk: Generated comparison stills may contain inaccurate small text or unverified product claims.

Mitigation: Use only seller-confirmed SKU facts, leave missing axes as gaps, and review printed rows against the confirmed spec list before delivery.

Risk: Billable image generation or edit requests can consume Beatra credits.

Mitigation: Show the production card with live model pricing before paid calls, use one opaque client request ID per still, submit each approved axis once, and report final net charged credits from returned billing fields.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/sku-comparison-chart)
- [Beatra Skill Homepage](https://beatra.ai/skills/sku-comparison-chart)
- [SKU comparison workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Beatra task outputs such as generated image artifacts, task IDs, resolved models, observed dimensions, and billed credit totals after user approval.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
