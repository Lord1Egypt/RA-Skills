## Description: <br>
Autonomous Solana wallet agent - AI reasons, Rust signs; supports transfers, swaps, staking, chat, and mode switching under constitutional spend limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neocryptoquant](https://clawhub.ai/user/Neocryptoquant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an OpenClaw-compatible agent to a local SONA Solana wallet service for wallet status checks, policy review, transfers, assisted approvals, chat commands, and mode switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can give an agent authenticated control over SONA wallet actions when SONA_TOKEN is configured. <br>
Mitigation: Install only when agent wallet control is intended; start with devnet or a low-value wallet and keep SONA_TOKEN secret. <br>
Risk: State-changing operations include transfers, chat-driven actions, mode switching, and assisted-mode approvals. <br>
Mitigation: Prefer standard or assisted mode, review pending action details before approval, and unset or rotate the token when finished. <br>


## Reference(s): <br>
- [SONA homepage](https://www.sonawallet.xyz) <br>
- [ClaWHub skill page](https://clawhub.ai/Neocryptoquant/sona) <br>
- [Publisher profile](https://clawhub.ai/user/Neocryptoquant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown responses, with setup guidance and command examples where applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses may include wallet status, SOL price, policy text, pending action details, approval status, transfer results, or error messages from the local SONA service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
