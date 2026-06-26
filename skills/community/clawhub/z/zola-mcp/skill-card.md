## Description: <br>
Connects an agent to Zola wedding planning data for vendors, budget, guests, RSVPs, seating, events, registry, gifts, and inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to access and manage Zola wedding planning data, including vendors, budgets, guests, seating, events, RSVPs, registry items, gifts, and vendor inquiries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires durable access to Zola account data through a long-lived refresh token or browser-cookie fallback. <br>
Mitigation: Treat the token like a password, avoid pasting or storing it unless necessary, and rotate or revoke it if exposed. <br>
Risk: The skill can support account-changing wedding planning actions and may activate for broad wedding-planning requests. <br>
Mitigation: Confirm the user intends to use Zola and review account-changing actions before they run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/zola-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to call Zola MCP tools that read or modify account data.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
