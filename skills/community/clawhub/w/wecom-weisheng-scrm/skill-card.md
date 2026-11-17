## Description:

Helps agents support WeCom customer operations by querying and managing Weisheng SCRM customers, tags, groups, campaign assets, live codes, mass messaging, follow-up records, conversations, opportunities, reports, lotteries, and schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangfang19](https://clawhub.ai/user/fangfang19)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-operations employees and teams use this skill through an agent to inspect Weisheng SCRM records, prepare campaign and customer-follow-up work, and perform confirmed business actions while respecting the current user's role and data scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live CRM data and can access broad SCRM capabilities through proxy calls.

Mitigation: Review before installing, use only on a trusted single-user machine, confirm user identity and role scope before business calls, and require explicit confirmation before uploads or write actions.

Risk: The skill stores an APP KEY and cached access tokens locally.

Mitigation: Treat the APP KEY like a password, do not provide APP KEY values from untrusted sources, avoid exposing credentials in logs or command output, and rotate the APP KEY if exposure is suspected.

Risk: Changing the base URL or disabling TLS verification can weaken request integrity.

Mitigation: Keep the default Weisheng endpoint and TLS verification enabled unless a trusted controlled environment explicitly requires otherwise.

Risk: Uploads and business write operations can change customer-operation records or publish uploaded assets.

Mitigation: Verify API documentation and collected parameters before execution, confirm the exact operation with the user, and do not automatically retry failed write operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fangfang19/skills/wecom-weisheng-scrm)
- [Publisher Profile](https://clawhub.ai/user/fangfang19)
- [Weisheng Open Platform](https://open.wshoto.com)
- [Claw API Summary](https://open.wshoto.com/doc/pages/claw/CLAW_SUMMARY.md)
- [Agent Runbook](artifact/references/agent-runbook.md)
- [User Guide](artifact/references/guide.md)
- [File Upload and Download Reference](artifact/references/file-utils.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Business-language responses with structured JSON command results and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public image URLs or file IDs after upload; write actions require explicit user confirmation and should not be automatically retried after failure.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter says 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
