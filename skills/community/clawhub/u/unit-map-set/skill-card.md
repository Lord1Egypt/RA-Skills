## Description:

Turn user-supplied unit outline points into one still per unit mind map page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and classroom-content creators use this skill to turn supplied unit titles, page names, and approved outline points into a page-ordered set of classroom mind-map stills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra device token grants broader account authority than classroom still-image generation requires, including other media scopes and wallet-spend scope.

Mitigation: Install only when that scope is acceptable, keep profile files private to the current user, and use the bundled disconnect workflow when the package is no longer needed.

Risk: Automatic updates can silently replace package-owned files after installation.

Mitigation: Disable automatic updates with scripts/mcp_client.py update --auto off when reviewed code must remain fixed, and use scripts/mcp_client.py update --check to inspect availability before updating.

Risk: Each approved page generation can spend Beatra credits and final charges may differ from the prepaid estimate.

Mitigation: Require the production card before billable calls, submit each page once with a unique client_request_id, and report billing.net_charged_credits from the completed task.

## Reference(s):

- [Unit-map workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and returned image artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one paid still-image generation task per approved unit page and reports task IDs, dimensions, resolved models, and net charged credits.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
