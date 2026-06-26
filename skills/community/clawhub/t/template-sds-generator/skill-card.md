## Description: <br>
Generate a deterministic, template-preserving 16-section SDS/MSDS package from 1 DOCX template, 1 prompt/rule file, and 1-3 source SDS/MSDS files, with DOCX/PDF output plus structured JSON, provenance CSV, and review checklist artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YJLi-new](https://clawhub.ai/user/YJLi-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and compliance teams use this skill to generate traceable SDS/MSDS output packages while preserving a supplied Word template. It is intended for draft generation with review artifacts that support human validation of safety-critical fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR can retain extracted SDS/MSDS text in a local cache. <br>
Mitigation: Use --enable-ocr only when scanned PDFs require it, and manage or delete the .cache/ocr directory for sensitive documents. <br>
Risk: Generated SDS/MSDS content may include safety-critical fields that require validation. <br>
Mitigation: Review structured_data.json, field_source_map.csv, and review_checklist.md before relying on the generated DOCX or PDF. <br>
Risk: Placeholder supplier and emergency-contact details may be unsuitable for production use. <br>
Mitigation: Replace config/fixed_company.yml with approved company information before relying on generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YJLi-new/template-sds-generator) <br>
- [OpenClaw homepage metadata](https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/template-sds-generator-skill) <br>


## Skill Output: <br>
**Output Type(s):** [files, markdown, structured JSON, CSV, DOCX/PDF] <br>
**Output Format:** [DOCX and optional PDF SDS document with structured JSON, provenance CSV, review checklist Markdown, and audit artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces final deliverables under outputs/runs/.../final and optional audit artifacts under outputs/runs/.../audit.] <br>

## Skill Version(s): <br>
0.2.1 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
