## Description:

Helps agents manage logistics records, generate bills of lading and customs documents, track shipment status, sync OKKI customer data, and prepare logistics reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, logistics coordinators, and developers use this skill to create shipment records, generate trade documents, archive bills of lading, send shipment notifications, and sync shipment follow-up data with OKKI CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact logistics and CRM actions may be exposed with weak scoping.

Mitigation: Require authentication and authorization for API and CLI workflows before use outside a controlled local environment.

Risk: Customer notifications and OKKI sync actions can affect external recipients and CRM records.

Mitigation: Validate recipients, review generated notification content, and restrict sync permissions to approved operators.

Risk: Bill-of-lading uploads and archive operations can write, read, copy, or delete local files.

Mitigation: Enforce upload size and type limits, sanitize filenames, and confine archive paths to an approved directory.

Risk: Temporary execution and external OKKI helper paths can introduce integrity and execution risk.

Mitigation: Use packaged or integrity-checked OKKI helpers and secure temporary-file handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-logistics-manager)
- [E2E test report](artifact/test/e2e_test_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON data, code snippets, and generated logistics document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local logistics records, document files, bill-of-lading archives, notification records, and OKKI sync logs.]

## Skill Version(s):

1.0.0 (source: server release evidence, target metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
