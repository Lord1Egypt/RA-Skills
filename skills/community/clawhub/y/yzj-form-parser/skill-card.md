## Description:

Parses YunZhijia form JSON and helps agents construct approval form payloads across main-form widgets, detail tables, attachments, images, people, departments, dates, and selection controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlifeng](https://clawhub.ai/user/jlifeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to interpret YunZhijia approval callback form data and build form JSON for approval initiation APIs. It is intended for workflows that need reliable handling of widgetMap, detailMap, and common YunZhijia control value formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated approval payloads or file-download examples may expose access tokens, personal identifiers, or tenant data if used without review.

Mitigation: Confirm authorization, use least-privilege tokens, avoid logging secrets or personal identifiers, and review generated requests before submitting them.

Risk: Incorrect widget value types, option keys, or detail-table mappings may create malformed or misleading YunZhijia form data.

Mitigation: Validate generated JSON against the target form definition and test with non-production data before using it in a real approval workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlifeng/skills/yzj-form-parser)
- [控件类型详解](references/widget-types.md)
- [明细表控件详解](references/detail-widget.md)
- [附件控件详解](references/file-widget.md)
- [YunZhijia file download endpoint](https://www.yunzhijia.com/docrest/doc/user/downloadfile)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, JSON, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON, Java, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; outputs should be reviewed before use with live YunZhijia tenants or approval APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
