## Description: <br>
Extract, store, and export tax documents (W-2, 1099-DA, all 1099 variants, K-1) using AI in a local-first web UI at localhost:8421. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DougButdorf](https://clawhub.ai/user/DougButdorf) <br>

### License/Terms of Use: <br>
MIT (core) <br>


## Use Case: <br>
External users and developers use TaxClaw to upload tax PDFs or images, extract structured fields, review low-confidence values, and export CSV or JSON for downstream tax workflows. It is a data extraction tool, not tax, legal, accounting, or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tax documents can contain SSNs, EINs, income records, and account data. <br>
Mitigation: Use Local mode by default, keep the local data directory protected, and verify every extracted value against the original document before use. <br>
Risk: Cloud mode sends document excerpts or images/content to Anthropic for AI processing. <br>
Mitigation: Enable Cloud mode only after accepting the privacy warning and only when the data owner accepts that third-party processing path. <br>
Risk: The localhost web UI loads a third-party script from unpkg. <br>
Mitigation: Review the web UI dependency path before deployment in sensitive environments, or vendor/pin the script under local control. <br>
Risk: AI extraction can produce incorrect, incomplete, or misleading tax fields. <br>
Mitigation: Treat outputs as draft structured data and require human review before tax filing, financial reporting, or sharing with a preparer. <br>
Risk: Uploaded originals and exports are retained locally and may be bundled into ZIP exports. <br>
Mitigation: Restrict file access to the TaxClaw data directory, delete unneeded documents through the UI or by removing the data directory, and share ZIP exports only with intended recipients. <br>


## Reference(s): <br>
- [ClawHub TaxClaw release page](https://clawhub.ai/DougButdorf/taxclaw) <br>
- [TaxClaw README](artifact/README.md) <br>
- [TaxClaw runbook](artifact/RUNBOOK.md) <br>
- [TaxClaw skill definition](artifact/SKILL.md) <br>
- [TaxClaw privacy policy](artifact/PRIVACY.md) <br>
- [TaxClaw terms of use](artifact/TERMS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files, structured data] <br>
**Output Format:** [Markdown guidance with inline shell commands; TaxClaw exports CSV, JSON, and ZIP files from the local app.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-provided tax documents locally by default and stores documents, extracted fields, and exports in the configured local data directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence; artifact frontmatter reports 0.1.0-beta) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
