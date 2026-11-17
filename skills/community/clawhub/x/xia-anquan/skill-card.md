## Description:

虾安全 — 基于腾讯/字节研究报告的 OpenClaw Agent 安全监控 skill。监控 CIK（Capability/Identity/Knowledge）三个维度，检测持久状态污染攻击、凭证外传、可疑脚本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit an OpenClaw workspace for CIK state-pollution risks across identity, knowledge, and capability files. It can run one-off checks, dimension-specific checks, or JSON-output audits for integration with other tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads OpenClaw workspace identity, memory, and skill script files and writes snapshots and logs that may contain sensitive workspace details.

Mitigation: Install only where local workspace scanning is acceptable, restrict access to ~/.cik-audit, and treat snapshots and logs as sensitive.

Risk: Real-time daemon monitoring is not reliable in the submitted artifact.

Mitigation: Use one-shot audit or JSON audit mode until monitor.cjs is fixed and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/xia-anquan)
- [Publisher profile](https://clawhub.ai/user/luis1213899)
- [Your Agent, Their Asset: A Real-World Safety Analysis of OpenClaw](https://arxiv.org/abs/2604.04759)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown-style console text and optional JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local snapshots and logs under ~/.cik-audit.]

## Skill Version(s):

1.0.0 (source: release evidence, artifact/_meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
