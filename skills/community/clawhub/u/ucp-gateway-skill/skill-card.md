## Description: <br>
MCP Tools skill for AI agent commerce that helps agents register or reuse a hosted UCP identity, search and compare products, prepare buyer-confirmed carts, and create merchant-hosted checkout handoff links without scraping or payment handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theagenttimes](https://clawhub.ai/user/theagenttimes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to connect to The Agent Times UCP Gateway for provider-neutral shopping search, cart creation or updates after buyer confirmation, and checkout handoff to merchant-hosted pages. It is intended for commerce workflows where agents need structured identity, live MCP tool schemas, and explicit operator confirmation before cart or checkout actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses helper scripts and outbound access to a hosted commerce gateway. <br>
Mitigation: Review the Python helper scripts before installation and use the skill only for intended commerce-gateway tasks. <br>
Risk: Local identity state under ./.ucpgateway may include private key material and registration details. <br>
Mitigation: Keep private_key.jwk local, avoid storing unrelated secrets or private data in the working directory, and send only public key material to the gateway. <br>
Risk: Cart and checkout handoff actions can affect purchase flows if used without clear buyer intent. <br>
Mitigation: Require explicit buyer or operator confirmation before cart changes and final checkout handoff, and present provider-returned totals, warnings, and merchant links for review. <br>
Risk: The skill supports checkout handoff but does not process payment or complete orders. <br>
Mitigation: Never collect payment credentials or claim payment completion; direct the buyer to enter payment details only on the merchant-hosted checkout page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theagenttimes/ucp-gateway-skill) <br>
- [UCP Gateway homepage](https://ucpgateway.theagenttimes.com/) <br>
- [UCP Gateway MCP endpoint](https://ucpgateway.theagenttimes.com/mcp) <br>
- [UCP Gateway source](https://github.com/theagenttimes/ucp-gateway-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON-RPC arguments, shell commands, and configuration file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse local ./.ucpgateway identity state and call the hosted UCP Gateway MCP service.] <br>

## Skill Version(s): <br>
0.2.3 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
