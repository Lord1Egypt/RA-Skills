## Description: <br>
Order food, groceries, and book restaurants in India via Swiggy's MCP servers with a safety-first confirmation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aditya4206360-prog](https://clawhub.ai/user/aditya4206360-prog) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to search Swiggy restaurants or groceries, build carts, preview costs and addresses, and place confirmed food, Instamart, or Dineout bookings in India. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: Orders and bookings can affect real purchases, delivery addresses, and restaurant reservations. <br>
Mitigation: Show the full cart or booking preview, including items, price, address, timing, and guests, and require explicit user confirmation before running commands with --confirm. <br>
Risk: The skill requires Swiggy authentication and shares search, cart, booking, location, and address details with Swiggy MCP services. <br>
Mitigation: Install only for users who accept that data sharing, complete OAuth intentionally, and avoid exposing credentials or account sessions to untrusted environments. <br>
Risk: Cash on Delivery orders cannot be cancelled after placement. <br>
Mitigation: Double-check the delivery address, order contents, price, and timing before approval, and do not proceed if any detail is uncertain. <br>
Risk: The security guidance notes a missing CLI implementation for npm link verification. <br>
Mitigation: Verify the CLI implementation from a trusted source before relying on npm link or using the global swiggy command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aditya4206360-prog/sr1) <br>
- [Swiggy Food MCP server](https://mcp.swiggy.com/food) <br>
- [Swiggy Instamart MCP server](https://mcp.swiggy.com/im) <br>
- [Swiggy Dineout MCP server](https://mcp.swiggy.com/dineout) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and order or booking previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before placing orders or bookings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
