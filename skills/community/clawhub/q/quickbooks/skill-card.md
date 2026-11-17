## Description:

Guides agents in managing QuickBooks Online accounting data through a user-authorized Maton connection, including reports and approved record changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting teams and their authorized agents use this skill to review QuickBooks customers, invoices, payments, and financial reports, and to make explicitly approved accounting changes or set up automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accounting writes or deletions may change financial records.

Mitigation: Use read-only operations by default; confirm the account, resource, amount, and consequence before each write or deletion.

Risk: An overly broad or wrong connection may expose unintended accounting data.

Mitigation: Use least-privileged authorization and verify the Maton account and QuickBooks connection before requests.

Risk: Persistent triggers or destinations may continue processing or forwarding data.

Mitigation: Enable them only with explicit approval and a clear understanding of their ongoing data flow.

## Reference(s):

- [QuickBooks skill release](https://clawhub.ai/byungkyu/skills/quickbooks)
- [Maton homepage](https://maton.ai)
- [Maton API documentation](https://docs.maton.ai/api-reference/overview)
- [QuickBooks Online API overview](https://developer.intuit.com/app/developer/qbo/docs/get-started)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authorized QuickBooks reads, writes, and optional scheduled or event-driven actions.]

## Skill Version(s):

1.2.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
