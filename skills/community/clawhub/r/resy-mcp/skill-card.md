## Description:

Manage Resy restaurant reservations via MCP by searching venues, booking tables, listing and canceling reservations, managing favorites, and subscribing to Priority Notify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a Resy MCP server for natural-language restaurant reservation workflows, including finding availability, booking, canceling, favorites, and Priority Notify subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned MCP package with live account access.

Mitigation: Prefer a pinned, reviewed local install over npx -y before connecting credentials.

Risk: Resy credentials are required and could be exposed if stored in project files or source control.

Mitigation: Store credentials outside shared project files, keep them out of source control, and restrict file permissions.

Risk: The MCP server can make real account changes, including bookings, cancellations, favorites, and Priority Notify subscriptions.

Mitigation: Require explicit user confirmation before actions that book, cancel, change favorites, or create notification subscriptions.

Risk: The server uses private Resy web-app endpoints that may change without notice.

Mitigation: Review failures carefully and revalidate behavior before relying on affected reservation workflows.

## Reference(s):

- [resy-mcp source repository](https://github.com/chrischall/resy-mcp)
- [resy-mcp npm package](https://www.npmjs.com/package/resy-mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate live Resy account actions through the configured MCP server.]

## Skill Version(s):

0.6.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
