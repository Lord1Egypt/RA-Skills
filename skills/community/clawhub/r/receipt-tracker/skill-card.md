## Description:

Extracts receipt data from photos, categorizes purchases, stores expenses in CSV, and produces monthly spending reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick4man](https://clawhub.ai/user/nick4man)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn receipt photos into categorized expense records and monthly spending summaries. It is suited for personal or household expense tracking workflows that can store purchase history in a local CSV file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes Nextcloud/WebDAV code with embedded credentials and a plaintext endpoint.

Mitigation: Remove hard-coded credentials, rotate the exposed password, require user-provided secrets, and use HTTPS before deployment.

Risk: Receipt photos and local expense history may contain sensitive personal purchase information.

Mitigation: Require clear user consent for external model analysis, minimize retained data, and protect access to expenses.csv.

Risk: The Nextcloud worker behavior is not fully disclosed by the main skill description.

Mitigation: Disclose the worker behavior clearly or disable it until the user configures the server, folder, credentials, and tagging workflow.

## Reference(s):

- [Receipt Tracker on ClawHub](https://clawhub.ai/nick4man/skills/receipt-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [JSON extraction results, CSV expense records, and Markdown spending reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses receipt photos as input and may append categorized expense rows to expenses.csv.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
