## Description:

管理体系内审不符合项判定与验证工具；适用于内审员需要录入不符合项、基于ISO条款辅助判定性质、跟踪验证状态或生成审核结论报告的场景

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Internal auditors and quality-management teams use this skill to record management-system nonconformances, classify findings against ISO clauses, track verification status, and generate audit conclusion reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled plaintext audit records may expose sensitive internal audit details to anyone with access to the skill package.

Mitigation: Review packaged records before installation, prefer an empty or synthetic datastore, and store live audit records outside the installed skill directory with documented retention and access controls.

## Reference(s):

- [ISO standard clause reference](references/iso_clauses.md)
- [Server-resolved GitHub source](https://github.com/duding-engicool/skill-nc-audit)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-nc-audit)
- [ClawHub publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON command output, and local report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts and JSON data files for nonconformance records, rule-based classification, verification updates, and report generation.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
