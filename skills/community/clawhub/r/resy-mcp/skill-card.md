## Description: <br>
Manage Resy restaurant reservations via MCP by searching venues, booking tables, listing and canceling reservations, managing favorites, and subscribing to Priority Notify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Resy MCP server for restaurant reservation workflows, including searching availability, booking or canceling tables, managing favorites, and managing Priority Notify subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Resy credentials. <br>
Mitigation: Use project-scoped MCP configuration where possible, avoid committing credentials, and protect RESY_EMAIL and RESY_PASSWORD as secrets. <br>
Risk: The connected MCP server can make real Resy account changes, including booking, canceling, changing favorites, and managing notifications. <br>
Mitigation: Require explicit user confirmation before actions that modify reservations, favorites, payment-linked booking state, or Priority Notify subscriptions. <br>
Risk: The artifact states that Resy does not publish an official API and that some endpoint paths are reverse-engineered. <br>
Mitigation: Treat failures or changed behavior as operational risk and verify actions in the Resy account after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/resy-mcp) <br>
- [resy-mcp npm package](https://www.npmjs.com/package/resy-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide setup of an MCP server that uses Resy credentials and can perform real account actions.] <br>

## Skill Version(s): <br>
0.5.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
