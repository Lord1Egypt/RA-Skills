## Description: <br>
MCP server for Underground Cultural District with developer utilities, marketplace browsing and search, x402 USDC purchase flows, receipt verification, persistent agent identity, and cross-agent messaging tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP server to run common utility tools, browse and search the Underground Cultural District catalog, retrieve free content, and initiate or verify wallet-mediated purchases. Agents can also use it for persistent identity storage and cross-agent message relay when that remote storage and messaging behavior is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote persistent identity storage may expose agent profile data beyond the local session. <br>
Mitigation: Use non-sensitive agent identifiers and avoid storing secrets, credentials, private workspace content, or sensitive personal data. <br>
Risk: Cross-agent messaging can relay user or agent-provided content through remote services with weakly described privacy and access boundaries. <br>
Mitigation: Treat relayed messages as external communications and review content before sending. <br>
Risk: Marketplace purchase and receipt tools can involve wallet-mediated USDC payments on Base or Solana. <br>
Mitigation: Require explicit user approval before initiating purchases, signing wallet authorizations, or verifying direct-transfer receipts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lisamaraventano-spine/underground-cultural-district) <br>
- [Underground Cultural District API](https://underground.substratesymposium.com) <br>
- [Substrate Symposium](https://substratesymposium.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill summary](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [MCP tool responses as plain text or JSON, with Markdown documentation and shell/configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some tools return remote content, delivery URLs, payment endpoints, receipt-verification results, identity records, or agent-message relay responses.] <br>

## Skill Version(s): <br>
4.5.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
