## Description: <br>
Analyze AWS Cost & Usage Reports to identify top cost drivers, waste, and anomalies across all linked accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and FinOps practitioners use this skill to analyze user-provided AWS billing exports or summarized spend data, identify major cost drivers and anomalies, and prioritize savings actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS billing exports can contain access keys, account IDs, resource names, tags, or other sensitive identifiers. <br>
Mitigation: Remove AWS access keys, secret keys, session tokens, unrelated identifiers, and sensitive tags before sharing data in the agent session. <br>
Risk: The skill includes AWS CLI examples that could expose billing and organization metadata if run with broad permissions. <br>
Mitigation: Run any CLI examples yourself using a least-privilege read-only AWS role, and share only the resulting exported data needed for analysis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anmolnagpal/spend-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, bullet lists, and inline AWS CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depends on user-provided AWS billing exports or summarized spend data; the skill does not directly access AWS.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
