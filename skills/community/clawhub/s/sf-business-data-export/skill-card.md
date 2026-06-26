## Description: <br>
Export Salesforce business data into business-readable Excel files from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evonne528](https://clawhub.ai/user/evonne528) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business analysts use this skill to turn Salesforce business questions into review-ready Excel exports with field catalogs, SOQL, validation summaries, and manifests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can export broad Salesforce business datasets into local Excel files if scope is left open. <br>
Mitigation: Before execution, explicitly set the Salesforce org, object list, date range, filters, profile or record type, and output directory; avoid full-scope exports unless they are intended. <br>
Risk: Using an over-privileged Salesforce account can expose more data than the business request requires. <br>
Mitigation: Run with a least-privileged Salesforce account that has only the object and field access needed for the requested export. <br>
Risk: Ambiguous page fields, record type, or profile context can produce incomplete or misleading review packages. <br>
Mitigation: Resolve page context before export, fall back only to explicit field lists when documented, and treat unresolved objects as failed rather than complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/evonne528/sf-business-data-export) <br>
- [End-to-End Usage](references/end-to-end-usage.md) <br>
- [Export Output Spec](references/export-output-spec.md) <br>
- [Review Package Format](references/review-package-format.md) <br>
- [Query Strategy](references/query-strategy.md) <br>
- [Page Field Collection SOP](references/page-field-collection-sop.md) <br>
- [Owner Polymorphism](references/owner-polymorphism.md) <br>
- [Parent Traversal Patterns](references/parent-traversal-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples plus generated CSV, JSON, SOQL, and XLSX artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces per-object field catalogs, SOQL files, Excel exports, validation results, and review manifests when Salesforce access and local output paths are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
