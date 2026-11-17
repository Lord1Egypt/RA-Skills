## Description:

Generate a deterministic, template-preserving 16-section SDS/MSDS package from 1 DOCX template, 1 prompt/rule file, and 1-3 source SDS/MSDS files, with DOCX/PDF output plus structured JSON, provenance CSV, and review checklist artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjli-new](https://clawhub.ai/user/yjli-new)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, safety-documentation teams, and regulatory operations users can use this skill to generate traceable SDS/MSDS document packages while preserving a supplied Word template. It is intended for workflows where generated DOCX/PDF files, structured data, source maps, and review checklists must be returned together.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic dependency bootstrap is incomplete or under-controlled for production installation.

Mitigation: Install only after the publisher provides a complete hashed lock file or a prebuilt runtime, and run the skill in an isolated workspace or container.

Risk: The default company configuration is a placeholder and could produce incorrect supplier information.

Mitigation: Replace config/fixed_company.yml with approved supplier information before producing real SDS documents.

Risk: Generated CSV and cached OCR/document data may create downstream safety or privacy exposure.

Mitigation: Treat generated CSV files as untrusted unless formula-sanitized, and disable or redirect OCR caching when source SDS files contain confidential supplier or formulation data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yjli-new/skills/template-sds-generator)
- [Project Homepage](https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/template-sds-generator-skill)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [DOCX/PDF files plus JSON, CSV, and Markdown audit artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+; OCR needs tesseract, and PDF export needs soffice or libreoffice.]

## Skill Version(s):

0.2.1 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
