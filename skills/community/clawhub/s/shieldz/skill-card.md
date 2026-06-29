## Description: <br>
Accept crypto payments with zero setup. Turn a wallet address into a shareable payment link or a reusable tip jar. Non-custodial, no account, no API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[denizyanbollu](https://clawhub.ai/user/denizyanbollu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to let an agent create non-custodial crypto payment links, reusable tip jars, and payment status summaries from a confirmed destination wallet address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends wallet addresses, payment amounts, memos, optional email addresses, and management tokens to Shieldz network services. <br>
Mitigation: Install only when that data sharing is acceptable, confirm each payment link or tip jar before creation, and avoid sending unnecessary optional fields. <br>
Risk: An incorrect or unconfirmed destination wallet address could route funds to the wrong recipient. <br>
Mitigation: Ask for a wallet address when missing and confirm the destination address with the user before creating a link. <br>
Risk: Management URLs and tokens can expose payment status and settlement details. <br>
Mitigation: Treat manage_url and manage_token values as private access links and share them only with authorized users. <br>


## Reference(s): <br>
- [Shieldz Agents](https://shieldz.cash/agents) <br>
- [Shieldz MCP Server](https://shieldz.cash/mcp) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash and JSON examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Shieldz payment URLs, embed snippets, management links, management tokens, and payment status summaries when the agent calls the service.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
