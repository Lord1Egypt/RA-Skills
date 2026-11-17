## Description:

Exports Salesforce business data from natural-language requests into business-readable Excel review packages with layout-visible fields, SOQL generation, relationship handling, SOAP query/queryMore export, and validation artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evonne528](https://clawhub.ai/user/evonne528)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external business reviewers, developers, and data operations teams use this skill to turn Salesforce export requests into review-ready Excel packages when standard Reports do not provide enough field coverage, row volume, or relationship handling. It is most useful for exports that need page-visible fields, owner or parent-owner context, polymorphic relationship handling, staged detail queries, and manifest-based validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Salesforce CRM data and can generate Excel, CSV, JSON, SOQL, and manifest files containing business records.

Mitigation: Run it only in controlled environments, use Salesforce accounts with appropriate export permissions, confirm object and field scope before execution, and treat all generated files as sensitive.

Risk: Auth JSON files and export logs may expose Salesforce access tokens or related authentication details if mishandled.

Mitigation: Use only trusted auth JSON files, restrict file access, avoid sharing authentication artifacts or raw logs, and rotate credentials if exposure is suspected.

Risk: Outbound Salesforce requests need host and redirect review to avoid unsafe destinations.

Mitigation: Review or patch the exporter to require Salesforce HTTPS hosts and block redirects or private destinations before real use.

Risk: Spreadsheet outputs can carry formula-injection risk when cell values are opened in Excel or similar tools.

Mitigation: Neutralize spreadsheet formulas before distributing generated Excel or CSV files.

## Reference(s):

- [End-to-End Usage](references/end-to-end-usage.md)
- [Export Output Spec](references/export-output-spec.md)
- [Query Strategy](references/query-strategy.md)
- [Page Field Collection SOP](references/page-field-collection-sop.md)
- [Review Package Format](references/review-package-format.md)
- [Owner Polymorphism](references/owner-polymorphism.md)
- [Parent Traversal Patterns](references/parent-traversal-patterns.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands plus generated SOQL, CSV, JSON, and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Salesforce authentication and trusted local inputs; review packages include per-object exports, field catalogs, validation results, and manifests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
