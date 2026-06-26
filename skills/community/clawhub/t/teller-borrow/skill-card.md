## Description: <br>
Expose the Teller delta-neutral and lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rbcp18](https://clawhub.ai/user/rbcp18) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to install, run, update, or register a Teller MCP server that exposes delta-neutral opportunities, borrow pool discovery, per-wallet loan terms, wallet loan views, and borrow or repay transaction builders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated borrow or repay transaction payloads could be incorrect, stale, or unsuitable for the user's intended chain, token, amount, spender, or loan terms. <br>
Mitigation: Review every generated transaction in the wallet before signing, including chain ID, contract addresses, approval spenders, amounts, and loan terms. <br>
Risk: Wallet and loan queries expose financial metadata to the configured Teller API endpoint. <br>
Mitigation: Use a trusted TELLER_API_BASE_URL and treat wallet addresses, loan details, and generated transaction data as sensitive financial metadata. <br>


## Reference(s): <br>
- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md) <br>
- [Teller Delta-Neutral API Reference](https://registry.scalar.com/@teller/apis/delta-neutral/latest) <br>
- [Teller Delta-Neutral API Base URL](https://delta-neutral-api.teller.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/rbcp18/teller-borrow) <br>
- [Publisher Profile](https://clawhub.ai/user/rbcp18) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool responses containing text plus structured JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool outputs may include prepared on-chain borrow or repay transaction payloads that require manual wallet review before signing.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
