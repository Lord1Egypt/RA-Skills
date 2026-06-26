## Description: <br>
Chat with Sally about metabolic health, blood sugar, A1C, nutrition, fasting, supplements, and lab results. Uses the Sally MCP server on Smithery with x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sally-labs](https://clawhub.ai/user/sally-labs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to ask Sally health-focused questions about metabolic health topics and receive cited responses through the Sally MCP tool. It is intended for knowledge-focused guidance, not diagnosis or replacement of professional medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup requires providing a dedicated wallet private key to Smithery for x402 paid calls. <br>
Mitigation: Use a separate low-balance wallet, avoid a main wallet, monitor transactions, and avoid placing private keys directly in shell history. <br>
Risk: Health-related questions are sent to Sally's backend through Smithery. <br>
Mitigation: Avoid identifying medical details and treat Sally's responses as knowledge-focused guidance rather than medical advice. <br>
Risk: Each use can trigger a micropayment from the configured wallet. <br>
Mitigation: Keep only limited funds in the wallet and review expected usage before invoking the tool repeatedly. <br>


## Reference(s): <br>
- [Sally AI Skill Page](https://clawhub.ai/sally-labs/sally-ai) <br>
- [Sally Website](https://asksally.xyz) <br>
- [Sally MCP Source](https://github.com/sally-labs/sally-mcp) <br>
- [Smithery Sally AI MCP Registry](https://smithery.ai/servers/sally-labs/sally-ai-mcp) <br>
- [x402 Protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves Sally response messages and citations from the MCP tool.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
