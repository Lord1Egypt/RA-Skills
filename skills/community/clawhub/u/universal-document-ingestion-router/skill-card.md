## Description:

Document parsing and knowledge-base import router.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to classify local documents, route them to suitable local parsers, and prepare standardized parsed packages for downstream knowledge-base ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated parsed artifacts can retain sensitive local document content.

Mitigation: Use a dedicated output directory, limit batch scope, and handle generated files as sensitive data.

Risk: Batch parsing can mix outputs when source names collide or broad private folders are selected.

Mitigation: Prefer isolated output directories for each run, use copied samples for tests, and review batch_summary.json before downstream ingestion.

Risk: CSV exports from untrusted spreadsheets can remain unsafe to open directly in spreadsheet tools.

Mitigation: Treat generated CSV files as untrusted and review them before opening or importing them elsewhere.

Risk: OCR or parser extraction can be empty or low quality for some image and scanned document inputs.

Mitigation: Check document.json status and quality warnings before indexing or relying on parsed output.

## Reference(s):

- [Architecture](references/architecture.md)
- [Agent Integration Notes](references/agent-integration.md)
- [Development Report](references/development-report.md)
- [ClawHub Skill Page](https://clawhub.ai/hollis9087/skills/universal-document-ingestion-router)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON manifests, Markdown content, JSONL chunks, CSV table exports, batch summaries, and concise shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parse attempts always emit document.json; successful text extraction may also emit document.md, chunks.jsonl, tables, or batch_summary.json.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
