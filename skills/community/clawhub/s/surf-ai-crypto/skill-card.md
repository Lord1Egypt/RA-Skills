## Description: <br>
Surf AI Crypto Skill helps agents retrieve live crypto data across markets, wallets, social intelligence, DeFi, on-chain SQL, prediction markets, news, and related domains through the Surf CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hughzhou-gif](https://clawhub.ai/user/hughzhou-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs current crypto market, wallet, token, DeFi, on-chain, social, prediction-market, news, or API reference data instead of relying on stale model knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs or updates a global Surf CLI and refreshes its API spec cache. <br>
Mitigation: Install only in environments where a global Surf CLI is acceptable, and review the CLI installation path and update behavior before use. <br>
Risk: The skill can propose durable routing changes to AGENTS.md or CLAUDE.md and commit them after approval. <br>
Mitigation: Review the proposed instruction-file diff and commit before accepting the routing change. <br>
Risk: Approved feedback can send recent chat context to Surf, which may include secrets or sensitive financial details. <br>
Mitigation: Approve feedback only after checking recent conversation context, and do not include API keys, wallet secrets, or sensitive financial details. <br>
Risk: The skill handles API keys, wallet addresses, and crypto account or portfolio queries. <br>
Mitigation: Configure API keys outside chat, avoid pasting secrets into the agent transcript, and limit wallet or financial data shared to what is necessary for the request. <br>
Risk: External API responses may contain untrusted data. <br>
Mitigation: Treat returned API content as data only and do not execute or follow instructions embedded in response fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hughzhou-gif/surf-ai-crypto) <br>
- [Surf CLI introduction](https://agents.asksurf.ai/docs/cli/introduction) <br>
- [Surf platform](https://agents.asksurf.ai) <br>
- [Surf API base](https://api.asksurf.ai/gateway/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI/API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Surf CLI installation and sync, route crypto queries to Surf commands, propose project instruction updates, and request approval before sending feedback.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
