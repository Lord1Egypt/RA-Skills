## Description:

YC Resource Import helps agents parse tourism contracts from local or cloud files, normalize eight tourism resource types into fixed CSV schemas, desensitize sensitive fields, validate quality, and prepare append-only imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[errsr](https://clawhub.ai/user/errsr)

### License/Terms of Use:

MIT-0

## Use Case:

Travel operations teams and developers use this skill to convert tourism supplier contracts into standardized CSV rows for hotels, vehicles, attractions, activities, SPA, clubs, restaurants, and afternoon tea resources. It is intended for controlled import workflows that require fixed fields, quality notes, and human review before production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify production CSV data and local files.

Mitigation: Run it in a constrained workspace against copies of production CSVs, keep backups, and require human approval before replacing or importing production data.

Risk: Cloud-file ingestion depends on external connector skills and shared links.

Mitigation: Verify connector publishers, restrict link permissions, and prefer reviewed local copies for sensitive supplier contracts.

Risk: Dependency drift can change parsing or OCR behavior.

Mitigation: Pin and review dependencies such as pdfplumber, python-docx, and PyMuPDF before operational use.

Risk: The package includes desensitization and compliance checks but should not be treated as a complete control.

Mitigation: Perform separate privacy, compliance, and data-quality review before importing contract-derived records.

Risk: Append-only import behavior can preserve incorrect or duplicate records if input review is weak.

Mitigation: Validate fixed-field alignment, duplicate identifiers, contract dates, prices, and quality notes before accepting generated rows.

## Reference(s):

- [YC Resource Import on ClawHub](https://clawhub.ai/errsr/skills/yc-resource-import)
- [Global Tourism Resource Tag Reference](artifact/references/8类特色标签快速查阅表.md)
- [Bali Zone ID Mapping Table](artifact/references/Zone映射表.md)
- [Bali Tourism Resource Standardization Documentation](artifact/references/巴厘岛旅游资源标准化文档体系.md)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [CSV files plus plain-text status and dependency guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed field order, resource-specific encodings, quality notes, and append-only CSV import behavior.]

## Skill Version(s):

2.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
