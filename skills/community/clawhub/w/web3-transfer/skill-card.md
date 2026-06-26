## Description: <br>
Unified multi-chain transfer skill for BTC, EVM, and Solana. Use when a user wants to send ETH/ERC20, SOL/SPL, or BTC, including batch payouts, with preview confirmation, wallet signing, risk checks, and status follow-up through the transfer-request / transfer-status / transfer-cancel MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this instruction-only skill to prepare BTC, EVM, and Solana transfers, review fees and recipient risk, collect confirmation, route wallet signing, and follow transfer status. It is intended for environments that expose the Antalpha transfer MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates crypto transfers through an external MCP transfer service, so users could expose funds to an untrusted service or signing flow. <br>
Mitigation: Install only if you trust Antalpha's MCP transfer service, review every wallet preview independently, and never sign a transaction unless the chain, token, amount, and recipient are correct. <br>
Risk: The registration flow returns an api_key that could be misused if stored casually. <br>
Mitigation: Store the registration api_key only in a secret store or similarly protected setting. <br>
Risk: Private keys, seed phrases, recovery phrases, and keystore files are highly sensitive and should never be shared with an agent or MCP service. <br>
Mitigation: Use only wallet-based signing flows and never provide private keys, seed phrases, recovery phrases, or keystore files. <br>
Risk: Some chain-specific safety checks are incomplete: Solana address security scanning is skipped in v1.0, and BTC address scanning may be marked as skipped. <br>
Mitigation: Disclose skipped scans, block HIGH or CRITICAL risk transfers, require explicit acknowledgement for MEDIUM risk or unavailable price data, and verify recipients in the user's own wallet before signing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deanpeng-dotcom/web3-transfer) <br>
- [deanpeng-dotcom publisher profile](https://clawhub.ai/user/deanpeng-dotcom) <br>
- [Antalpha transfer MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp) <br>
- [Antalpha](https://antalpha.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API Calls] <br>
**Output Format:** [Markdown guidance with MCP tool-call instructions and concise user-facing transfer status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; coordinates transfer previews, wallet signing links, BTC PSBT handoff, cancellation, and status follow-up through runtime-provided MCP tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
