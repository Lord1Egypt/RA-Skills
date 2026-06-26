## Description: <br>
Parses resumes from PDF, Word, and image files into structured data, analyzes fit against job descriptions, and generates resume improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayalili](https://clawhub.ai/user/Ayalili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and recruiting workflow users can use this skill to extract structured resume fields, compare a resume with a job description, and produce targeted improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes resumes and can expose sensitive personal data such as contact details, age, gender, work history, and education history. <br>
Mitigation: Use only resumes the operator is authorized to process, redact unnecessary personal fields where possible, and avoid retaining generated JSON or prompts longer than needed. <br>
Risk: The artifact claims local-only processing, but security evidence says model and data handling are unclear. <br>
Mitigation: Confirm the language model backend is truly local and offline before supplying real personal data. <br>
Risk: Job-fit scoring and resume suggestions may be incomplete or misleading if extracted resume text, OCR output, or job-description interpretation is wrong. <br>
Mitigation: Review extracted fields, scores, missing requirements, and suggestions before using them in hiring or candidate-facing workflows. <br>


## Reference(s): <br>
- [Field Extraction Guide](artifact/references/field_extraction_guide.md) <br>
- [Resume Matching Rules](artifact/references/matching_rules.md) <br>
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON, Markdown-style analysis, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include extracted personal data, job-match scores, analysis, and generated prompts for a language model.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
