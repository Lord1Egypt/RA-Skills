## Description:

Turn user-supplied session names and themes into a four-to-eight still wealth cover set. This session cover set studio lays out each named investor education cover as its own still. Use it for session cover stills, education session covers, and a matching cover pack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creative teams use this skill to plan and generate a coordinated set of investor-education session cover stills from user-supplied session names and themes. It produces a free pack plan before any billable image generation and then creates one approved still per named session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a broad shared Beatra device token with media, upload, task, and wallet permissions.

Mitigation: Review before installing and use it only with a Beatra account where those permissions are acceptable.

Risk: The bundled client can silently replace package-owned code through automatic updates.

Mitigation: Disable automatic updates when reviewed code must remain fixed.

Risk: Billable image generation can create duplicate charges if uncertain requests are replayed incorrectly.

Mitigation: Use one opaque client_request_id per approved still and retry only an identical frozen payload with the same request identity.

Risk: Generated cover text may be incorrect or unreadable, especially small type.

Mitigation: Review visible printed lines against the confirmed pack list and report unreadable text as a review item.

## Reference(s):

- [Wealth cover pack workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/wealth-cover-set)
- [Beatra skill homepage](https://beatra.ai/skills/wealth-cover-set)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown prose with command snippets, generated image artifact references, task IDs, dimensions, formats, resolved models, and billing totals when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans four to eight stills by default, one generated still per named session, and caps the pack at eight.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
