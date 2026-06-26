## Description: <br>
Solana wallet-native AI gateway - pay per AI request with USDC on Solana across multiple AI providers without provider API keys or accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yebdmo2](https://clawhub.ai/user/yebdmo2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to access AI inference, orchestration, and related capabilities through SolanaProx using a Solana wallet address and pre-funded USDC balance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a Solana wallet address to solanaprox.com as the credential for paid AI requests. <br>
Mitigation: Use a dedicated wallet or low-balance account and only install the skill if sending that wallet address to SolanaProx is acceptable. <br>
Risk: Automated or unattended orchestration can spend from a pre-deposited USDC balance. <br>
Mitigation: Monitor spending and avoid unattended use unless explicit cost controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yebdmo2/solanaprox-ai) <br>
- [SolanaProx homepage](https://solanaprox.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include wallet-address configuration and examples for paid SolanaProx API requests.] <br>

## Skill Version(s): <br>
4.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
