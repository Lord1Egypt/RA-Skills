## Description:

Turn user-supplied risk-grade definitions into a four-to-eight still risk grade set. This risk grade still studio lays out each named grade as its own still. Use it for risk grade graphics, risk level cards, risk classification stills, and a risk grade pack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn user-approved risk-grade definitions into a coordinated four-to-eight pack of still images, with one still per grade. It is intended for risk-grade graphics and classification cards, not certified ratings, market data, or investment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a broad shared Beatra device authorization for media, task, artifact, wallet, and generation capabilities.

Mitigation: Authorize only from an account where these capabilities and possible credit use are acceptable, keep the token in the private credential file, and revoke or uninstall the connection when it is no longer needed.

Risk: The bundled client can silently replace package-owned files through automatic updates.

Mitigation: Disable automatic updates after installation when change control is required, and use the packaged update check before accepting a newer release.

Risk: Generated stills may contain unreadable or incorrect small text, or be mistaken for certified ratings or investment recommendations.

Mitigation: Review visible printed text against the confirmed pack list and present outputs as risk-grade graphics only, not as certified ratings, market data, or buy/sell advice.

Risk: Billable generation charges can differ from the prepaid estimate and duplicate submissions can create duplicate work.

Mitigation: Show the production card before paid calls, use one opaque client_request_id per still, avoid resubmitting running tasks, and report billing.net_charged_credits from the completed task.

## Reference(s):

- [Risk-grade pack workflow](references/workflow.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Installation and authentication](references/installation-and-auth.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a pack plan and Beatra task/result reporting; image artifacts are created through Beatra after explicit approval and billing.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
