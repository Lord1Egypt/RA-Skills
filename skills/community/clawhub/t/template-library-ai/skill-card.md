## Description: <br>
Templatebased Writing helps users select, create, upload, fill, and generate DOCX or PPTX documents from built-in or user-supplied templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yueheng-rgb](https://clawhub.ai/user/yueheng-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather document requirements, choose or create templates, collect content, and produce formatted documents such as theses, reports, resumes, and presentation decks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user documents, personal details, API keys, and payment-verification data to a third-party remote service over plain HTTP. <br>
Mitigation: Use only with non-confidential documents unless the service uses HTTPS and publishes clear retention and deletion terms. <br>
Risk: The workflow gives the agent authority to initiate payment and submit payment-verification data. <br>
Mitigation: Require explicit user confirmation before payment, verify the amount and recipient, and avoid sharing payment proof beyond the documented verification step. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yueheng-rgb/template-library-ai) <br>
- [README](artifact/readme.md) <br>
- [API Reference](artifact/references/api.md) <br>
- [Pricing Reference](artifact/references/pricing.md) <br>
- [Template Reference](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples; generated document paths or download links may point to DOCX, PPTX, or PDF outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require TEMPLATE_API_KEY, user document uploads, and payment-verification data.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
