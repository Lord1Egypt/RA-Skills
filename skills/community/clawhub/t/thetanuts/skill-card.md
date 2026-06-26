## Description: <br>
Trade crypto options on Thetanuts Finance with orderbook fills, RFQ lifecycle, multi-strike structures, real-time WebSocket, wallet management, early settlement, and referrer fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goheesheng](https://clawhub.ai/user/goheesheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to manage a dedicated crypto wallet, inspect Thetanuts Finance option markets and positions, and prepare or execute crypto options trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores wallet seeds in plaintext and requires sensitive wallet credentials. <br>
Mitigation: Use only a fresh, low-value dedicated wallet, never import a primary seed, and treat ~/.openclaw/wdk-mcp/.env as a full wallet secret. <br>
Risk: The skill can approve tokens, sign messages, and broadcast wallet transactions on mainnet. <br>
Mitigation: Review every approval, signature, and transaction before broadcast because mainnet actions can cause irreversible financial loss. <br>
Risk: The release evidence flags an unsafe remote updater. <br>
Mitigation: Run updates only after explicit user consent and manually inspect update output and changed code before applying it. <br>
Risk: Logs or shared transcripts may expose seed phrases, wallet balances, or other financial information. <br>
Mitigation: Avoid sharing logs or conversation excerpts that contain wallet secrets, addresses, balances, or transaction details. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/goheesheng/thetanuts) <br>
- [Thetanuts Finance](https://thetanuts.finance) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and transaction review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet, balance, market, RFQ, approval, signature, and transaction guidance for a local OpenClaw environment.] <br>

## Skill Version(s): <br>
1.5.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
