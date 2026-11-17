## Description:

WorkBuddy 安全稳定运行专家团（WB-SAFE）helps agents assess credential safety, token cost, connector health, configuration drift, encryption posture, system health, operational risk, and disaster recovery for AI workbench environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run structured safety and stability checks for WorkBuddy-style agent workspaces, including credential exposure review, usage governance, connectivity checks, baseline drift review, local health checks, and recovery planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output can reveal where credentials or sensitive configuration files are located.

Mitigation: Treat generated reports as sensitive and share only redacted paths or summaries when collaborating.

Risk: Recovery rehearsal can copy identity, memory, connector metadata, and snapshot files into a temporary sandbox.

Mitigation: Run wb_recovery_full.py in dry-run mode first and use --execute only after reviewing the scope and accepting the temporary copy behavior.

Risk: The skill includes local scripts that inspect workspace files and system health.

Mitigation: Run scripts only against WorkBuddy or workspace directories the user intends to inspect, and review script scope before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/wb-safe-team)
- [八条防线速查表](references/eight-lines-defense.md)
- [安全体检 SOP 手册](references/safety-check-sop.md)
- [配套脚本使用指南](references/scripts-guide.md)
- [安全审计报告](安全审计报告.md)
- [Security test results](security_results.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with optional local script commands and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first workflow; audit scripts report credential locations without echoing secret values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
