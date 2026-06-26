## Description: <br>
Audit AWS resource tagging compliance and identify unallocatable spend for FinOps teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
FinOps teams, cloud governance reviewers, and AWS operators use this skill to analyze exported AWS resource, tag, and cost data for tagging compliance, unallocatable spend, and remediation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS tag, resource, and cost exports may include sensitive operational or billing details. <br>
Mitigation: Share only the exports needed for the audit and review data before pasting it into the chat session. <br>
Risk: Generated SCPs, AWS Config rules, or tagging commands may affect AWS account behavior if applied without review. <br>
Mitigation: Manually review proposed policies, rules, and commands before applying them to an AWS account. <br>
Risk: Credentials or secret keys could be accidentally included when users provide raw AWS data. <br>
Mitigation: Do not provide AWS credentials or secret keys, and confirm pasted data excludes credentials before analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/tagging-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with scoring, tables, JSON snippets, policy snippets, and AWS CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output based on user-supplied AWS exports or descriptions; does not access AWS directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
