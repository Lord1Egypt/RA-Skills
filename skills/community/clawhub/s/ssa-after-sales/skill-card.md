## Description:

After-sales Service manages customer complaints, repeat-order quotes, satisfaction surveys, analytics reports, and OKKI CRM synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and customer-support or sales operations teams use this skill to track after-sales complaints, repeat-order opportunities, satisfaction data, and operational reports. It can also sync selected complaint and repeat-order records into OKKI CRM as after-sales follow-up entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public OKKI sync routes can mutate CRM data or expose sync state without access control.

Mitigation: Require authentication and authorization on all HTTP routes before enabling the OKKI API integration.

Risk: Complaint and repeat-order details can be sent to OKKI CRM without an explicit user confirmation or privacy notice.

Mitigation: Add clear confirmation prompts and privacy notices before syncing customer records to OKKI.

Risk: The OKKI fallback path generates and executes temporary Python source, which increases execution and temporary-file handling risk.

Mitigation: Remove dynamic Python source generation; use a fixed audited helper with stdin or JSON IPC and secure temporary-file handling if temporary files remain necessary.

Risk: Raw sync logs and error details may expose customer identifiers, CRM identifiers, or operational diagnostics.

Mitigation: Restrict log access and redact sensitive fields from public responses and CLI output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-after-sales)
- [Publisher profile](https://clawhub.ai/user/cjboy007)
- [E2E test report](artifact/test/e2e_test_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include after-sales records, analytics summaries, OKKI sync status, and sync logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
