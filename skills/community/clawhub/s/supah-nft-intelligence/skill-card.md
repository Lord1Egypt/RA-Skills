## Description: <br>
NFT collection tracking, whale monitoring, and portfolio valuation for Base blockchain. Track floor prices, whale moves, and discover undervalued collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query SUPAH NFT intelligence for Base blockchain collections, including floor prices, whale movement, rarity, collection analytics, sale alerts, and portfolio valuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 requests can incur USDC charges when the skill or alert behavior calls the external SUPAH API. <br>
Mitigation: Use a dedicated low-balance wallet or strict spending limits, and require explicit confirmation before paid requests or sale alerts are enabled. <br>
Risk: The skill sends collection or wallet queries to api.supah.ai for NFT analytics. <br>
Mitigation: Review intended outbound data before use and avoid sending wallet or collection identifiers that should not be shared with the external service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/supah-based/supah-nft-intelligence) <br>
- [Publisher Profile](https://clawhub.ai/user/supah-based) <br>
- [SUPAH Website](https://supah.ai) <br>
- [SUPAH API Endpoint](https://api.supah.ai) <br>
- [x402 Documentation](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and concise text guidance from command-line or agent-invoked NFT analytics requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound network access to api.supah.ai, Node.js execution, and SUPAH_API_BASE configuration when overriding the default API endpoint.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
