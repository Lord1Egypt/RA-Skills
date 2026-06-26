## Description: <br>
Generates structured meeting minutes from PDF or Word meeting transcripts using multi-pass extraction, validation, and output formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crayfish153](https://clawhub.ai/user/crayfish153) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external teams use this skill to turn raw meeting transcripts into complete, structured meeting minutes with topics, decisions, details, and formatted deliverables. It is suited to PDF or Word transcripts that need detailed notes, completeness checks, and optional PDF or Word output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts may contain confidential, personal, or regulated information that could be processed by an external AI service. <br>
Mitigation: Redact sensitive content before use and confirm that organizational policy permits third-party AI processing for the transcript. <br>
Risk: Generated names, numbers, decisions, deadlines, action items, and company-name validations may be inaccurate or incomplete. <br>
Mitigation: Manually verify the final notes against the original transcript before sharing or relying on them. <br>


## Reference(s): <br>
- [AI prompt templates](references/ai-prompts.md) <br>
- [Meeting notes output format specifications](references/format-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [Structured meeting minutes in text, PDF, or Word format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a four-pass extraction, comparison, supplementation, and final review process; default output targets detailed notes of at least 2000 words or characters when source content supports it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
