## Description: <br>
AI Agent Skill for GitHub project analysis and nad.fun token launch. Analyzes repos, generates token identity/promo, and launches on nad.fun. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starrftw](https://clawhub.ai/user/starrftw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and builders use Tokenbroker to analyze GitHub projects, generate token identity and promotional materials, and prepare nad.fun launch assets for review and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mainnet-capable token launch preparation and external upload or transaction steps can create irreversible financial exposure. <br>
Mitigation: Use testnet first and require explicit approval before external uploads, public posting, or any mainnet transaction. <br>
Risk: Wallet keys, GitHub tokens, and nad.fun API keys may be exposed if handled outside the intended local environment. <br>
Mitigation: Avoid primary wallets and raw private keys, restrict GitHub token scope, and keep credentials in local environment variables or an excluded .env file. <br>
Risk: Generated token metadata and promotional copy may contain unsupported claims or misleading financial language. <br>
Mitigation: Review all generated token metadata and promotional content before publication. <br>
Risk: Cross-skill delegation can trigger actions in other skills without enough user awareness. <br>
Mitigation: Require explicit approval before delegating launch, wallet, posting, or safety-review actions to other skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/starrftw/tokenbroker) <br>
- [Tokenbroker Skill Definition](artifact/SKILL.md) <br>
- [Setup Guide](artifact/SETUP.md) <br>
- [Project Scan Guide](artifact/PROJECT-SCAN.md) <br>
- [Token Metadata Guide](artifact/METADATA.md) <br>
- [Launch Orchestration Guide](artifact/LAUNCH.md) <br>
- [Promotion Guide](artifact/PROMO.md) <br>
- [Builder Reputation Guide](artifact/STATS.md) <br>
- [nad.fun Skill Reference](https://nad.fun/skill.md) <br>
- [Monad Development Skill Reference](https://gist.github.com/moltilad/31707d0fc206b960f4cbb13ea11954c2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-like launch metadata, TypeScript examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project scan summaries, token metadata proposals, promotional drafts, and launch-preparation guidance for agent review workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
