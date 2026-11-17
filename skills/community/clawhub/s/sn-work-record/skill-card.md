## Description:

蜀宁 OA 工时与报销：填报/修改/查询工时，查看报销申请状态与审批进度；删除与恢复暂禁。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ithou](https://clawhub.ai/user/ithou)

### License/Terms of Use:

MIT-0

## Use Case:

OA users and assistants use this skill to query and summarize work records and reimbursement approval progress, and to submit or update work entries when authorized. Deletion and restoration are currently disabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment notes a mismatch between deletion/restoration capabilities flagged by the scan and the skill's stated disabled status.

Mitigation: Keep deletion and restoration unavailable as documented, and confirm the installed release's behavior before use involving record changes.

Risk: Release guidance contains an unpinned release-tool command, and the security assessment has medium confidence with a recorded scanner exit-status error.

Mitigation: Review and pin the release tool before publishing; treat the benign verdict as limited assurance and inspect the exact release security report.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ithou/skills/sn-work-record)
- [Query workflow](references/query-workflow.md)
- [Write workflow](references/write-workflow.md)
- [Reimbursement query and display](references/reimbursement-query.md)
- [Authentication and runtime](references/authentication-runtime.md)
- [Deletion and recovery restrictions](references/deletion-recovery.md)
- [Security revision 1.15.1](references/security-revision-1.15.1.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Chat summaries and structured JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Credentials and internal identifiers are withheld by default; write actions require explicit authorization and verification.]

## Skill Version(s):

1.15.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
