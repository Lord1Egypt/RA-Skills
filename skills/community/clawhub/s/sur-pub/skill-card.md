## Description: <br>
Create and trade tokens on SURGE via API with server-managed wallets, one-time free funding, and auto-routed pre-DEX and post-DEX trading on EVM (Base) or Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nkhromovweway](https://clawhub.ai/user/nkhromovweway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide token creation, wallet setup, funding, and trading through the SURGE development API. The skill helps an agent collect required launch information, confirm irreversible actions, and translate API errors into user-facing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use a raw API key for token launches and trades involving crypto assets. <br>
Mitigation: Use a dedicated, revocable, least-privilege API key where available, keep balances small, and revoke the key when finished. <br>
Risk: Token launches and trades can be irreversible and may involve financial loss. <br>
Mitigation: Require explicit user confirmation for every launch and trade amount, and review wallet, chain, token, and amount details before execution. <br>
Risk: The release is for a development SURGE API endpoint and may not reflect production behavior. <br>
Mitigation: Use it only when intending to operate the SURGE development workflow and verify live fees, chains, and limits through the launch-info endpoint before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nkhromovweway/sur-pub) <br>
- [SURGE application](https://app.surgedevs.xyz) <br>
- [SURGE development API base URL](https://back.surgedevs.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided SURGE API key and explicit user confirmation before token launch.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
