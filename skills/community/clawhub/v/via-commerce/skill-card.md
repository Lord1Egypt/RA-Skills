## Description: <br>
Agentic commerce over the VIA network for discovering products and sellers, submitting buyer briefs, finding live buyer demand, registering stores, and guiding USDC settlement on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardjhobbs](https://clawhub.ai/user/richardjhobbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to find products, compare VIA sellers, submit buyer briefs, discover buyer demand, register stores, and guide commerce actions that require explicit approval before payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commerce flows involving wallet details, dashboard credentials, seller MCP connections, and USDC payment delegation. <br>
Mitigation: Use it only for VIA commerce, require the agent to show prices and options, and give explicit approval before any purchase or payment action. <br>
Risk: The agent might overstate availability after a narrow or zero-result search. <br>
Mitigation: Broaden or clarify searches before treating an item as not found, and present multiple matching products side by side when available. <br>
Risk: A purchase could exceed the user's intended spending limit. <br>
Mitigation: Confirm the price before payment and never exceed any user-set delegation cap. <br>


## Reference(s): <br>
- [VIA Network MCP endpoint](https://app.getvia.xyz/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment-related actions require explicit user approval and must respect any delegation cap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
