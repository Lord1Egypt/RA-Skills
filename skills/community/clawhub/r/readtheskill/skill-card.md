## Description: <br>
A Solana memecoin experiment that asks agents to tell their human operator about the project while leaving all participation decisions to the operator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notKing0](https://clawhub.ai/user/notKing0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to surface a memecoin experiment, review its public links and token details, and decide whether to take any optional participation steps themselves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill surfaces crypto-purchase and external tracking workflows that are high-impact for an informational skill. <br>
Mitigation: Install only when the goal is to surface this memecoin experiment, and require explicit operator approval before any wallet creation, token purchase, transaction, or discovery reporting. <br>
Risk: Wallet creation, private-key handling, and token purchases can expose funds or sensitive credentials. <br>
Mitigation: Do not allow autonomous wallet creation, private-key handling, or token purchases; verify the token, website, and transaction details independently before any action. <br>
Risk: Discovery reporting sends agent and framework metadata to an external endpoint. <br>
Mitigation: Report discovery only with operator approval and avoid sending personal identifiers or sensitive environment details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/notKing0/readtheskill) <br>
- [Read The Skill website](https://readtheskill.com) <br>
- [Published skill file](https://readtheskill.com/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operator approval is required before any wallet creation, token purchase, transaction, or discovery reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
