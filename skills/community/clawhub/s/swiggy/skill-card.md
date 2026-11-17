## Description:

Order food, groceries, and book restaurants in India via Swiggy's MCP servers. Food delivery, Instamart groceries, and Dineout restaurant bookings with safety-first confirmation workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regalstreak](https://clawhub.ai/user/regalstreak)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search Swiggy restaurants or Instamart products, manage carts, and book Dineout reservations in India. The intended workflow previews carts or booking details and requires explicit user confirmation before orders or bookings are placed.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The server security review reports that the CLI unsafely builds shell commands from user-controlled input.

Mitigation: Review before installing or using, and do not pass untrusted or copied text into the CLI until command execution is changed to an argument-array API with shell disabled.

Risk: Searches, locations, addresses, cart contents, and booking or order details are sent to Swiggy MCP servers.

Mitigation: Use only with accounts and data the user is comfortable sharing with Swiggy, and confirm the environment uses a compatible patched Clawdbot version.

Risk: The artifact states that orders currently use Cash on Delivery and cannot be cancelled once placed.

Mitigation: Show the cart or booking preview, delivery address, total, and timing details, then require explicit user confirmation before invoking an order or booking command.

## Reference(s):

- [ClawHub Swiggy Skill Page](https://clawhub.ai/regalstreak/skills/swiggy)
- [Swiggy MCP Server Manifest](https://github.com/Swiggy/swiggy-mcp-server-manifest)
- [Swiggy Food MCP Server](https://mcp.swiggy.com/food)
- [Swiggy Instamart MCP Server](https://mcp.swiggy.com/im)
- [Swiggy Dineout MCP Server](https://mcp.swiggy.com/dineout)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18, mcporter, an active internet connection, and Swiggy OAuth authentication.]

## Skill Version(s):

1.0.5 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
