## Description: <br>
Creates and manages Solana token price alerts so users can be notified when a token price rises above or falls below a target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liji3597](https://clawhub.ai/user/liji3597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to create, list, delete, and manually check Solana token price alerts. It supports above/below threshold alerts, stop-loss alerts, take-profit alerts, and bilingual script output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alert creation, deletion, listing, and global notification checks may lack visible authorization boundaries in a multi-user deployment. <br>
Mitigation: Install only where the surrounding OpenClaw service enforces alert ownership for every user ID and restricts global price checks to a trusted scheduler or administrator. <br>
Risk: Price alerts can create misleading trading expectations if treated as predictions or advice. <br>
Mitigation: Use the skill only to record alert thresholds, keep confirmation prompts before creation or deletion, and preserve the guardrail against price prediction. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liji3597/solana-alerts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text or JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SOLANA_NETWORK; user-facing output may be Chinese or English.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
