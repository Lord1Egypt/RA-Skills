## Description: <br>
Resume-to-Tags turns resume text or files into a searchable candidate tag matrix by generating an LLM extraction prompt, expanding tags with synonyms, and guiding Feishu Bitable record creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, HR teams, and talent operations users can use this skill to standardize resumes into atomic school, company, skill, tool, domain, language, certificate, and experience tags for search and candidate matching. It also guides creation of a Feishu Bitable candidate tag database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume inputs and generated outputs can contain candidate contact details and raw resume content. <br>
Mitigation: Use only resumes the operator is authorized to process, redact contact details before sharing outputs, and apply retention and access controls for candidate data. <br>
Risk: The workflow can write candidate records into a Feishu Bitable workspace. <br>
Mitigation: Confirm the exact Feishu workspace, app, table, and access permissions before creating or batch-inserting records. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tuobadaidai/resume-to-tags) <br>
- [references/synonyms.json](references/synonyms.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated extraction prompts may include resume excerpts up to 5000 characters and basic contact details detected from the input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
