## Description: <br>
Escrow as a Service for AI agents. Create trustless USDC escrow transactions on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xasus1](https://clawhub.ai/user/Xasus1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents, developers, and operators use this skill to register a Trustra-managed wallet and run buyer or seller USDC escrow workflows for agent-to-agent transactions on Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move escrow funds through pay, release, withdraw, cancel, and dispute actions. <br>
Mitigation: Require explicit human approval before executing fund-moving commands and keep only minimal funds in the managed wallet. <br>
Risk: The skill stores and can export sensitive wallet and API credentials. <br>
Mitigation: Protect credentials.json and TRUSTRA_API_KEY, and avoid running export_key.py in autonomous or logged workflows. <br>
Risk: Use depends on Trustra's API, managed-wallet model, and dispute process. <br>
Mitigation: Install and use the skill only after confirming trust in Trustra's service model and operational process. <br>


## Reference(s): <br>
- [Trustra Escrow ClawHub page](https://clawhub.ai/Xasus1/trustra-escrow) <br>
- [Trustra homepage](https://trustra.xyz) <br>
- [Trustra API base](https://api.trustra.xyz/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON credential examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create credentials.json, print wallet or API details, and call Trustra escrow/payment endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
