## Description:

Scan bank statements to detect recurring charges, flag suspicious transactions, and draft refund requests with interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreolf](https://clawhub.ai/user/andreolf)

### License/Terms of Use:

MIT

## Use Case:

External users and personal finance reviewers use this skill to analyze bank or card transaction exports, identify recurring or suspicious charges, and prepare refund or dispute request drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial reports and raw analysis files may store sensitive transaction details locally under ~/.refund_radar.

Mitigation: Confirm the user is comfortable with local storage, restrict file permissions where appropriate, and remove reports or raw exports when they are no longer needed.

Risk: The HTML report template embeds an external footer link even though the skill claims local-only behavior.

Mitigation: Review or remove the footer link before opening or sharing generated reports.

Risk: The artifact describes running a refund_radar Python module but does not include that implementation.

Mitigation: Verify the installed refund_radar module and its source before executing commands against financial data.

## Reference(s):

- [Detection Rules Reference](references/detection-rules.md)
- [Refund Template Reference](references/refund-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, refund request drafts, and local HTML or JSON report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated refund text should avoid apostrophes, and reports may include privacy toggles, copy buttons, and collapsible sections.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact documentation lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
