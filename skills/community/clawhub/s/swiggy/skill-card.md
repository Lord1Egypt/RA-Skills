## Description: <br>
Order food, groceries, and book restaurants in India via Swiggy's MCP servers, with a safety-first confirmation workflow for Food Delivery, Instamart groceries, and Dineout restaurant bookings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regalstreak](https://clawhub.ai/user/regalstreak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and end users in India use this skill to search Swiggy food delivery, Instamart groceries, and Dineout restaurants, then build carts or bookings for user review. The skill is intended to place orders or bookings only after explicit confirmation of the cart, address, total, and booking details. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a command-injection risk from user-controlled order or search text passed through the CLI. <br>
Mitigation: Review carefully before installing; avoid untrusted or pasted user input until the mcporter invocation uses an argument-array API such as execFileSync or spawn. <br>
Risk: Food and grocery orders are Cash on Delivery only and cannot be cancelled once placed. <br>
Mitigation: Preview all items, quantities, prices, totals, delivery address, and timing before using the required --confirm flag. <br>
Risk: OAuth authentication can act on the connected Swiggy account. <br>
Mitigation: Authenticate only the intended Swiggy account and review every cart, address, total, and booking detail before confirming. <br>


## Reference(s): <br>
- [Swiggy ClawHub page](https://clawhub.ai/regalstreak/swiggy) <br>
- [Swiggy MCP server manifest](https://github.com/Swiggy/swiggy-mcp-server-manifest) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown instructions with shell command examples and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the mcporter skill, OAuth authentication with a Swiggy account, and explicit confirmation before order or booking commands.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
