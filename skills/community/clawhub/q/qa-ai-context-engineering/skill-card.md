## Description: <br>
Packages prior QA analysis, such as requirement decomposition, scenario trees, boundary lists, and risk assessment, into a structured AI context package for generating test cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers and test-focused agents use this skill after requirements and scenario analysis to prepare a complete business, functional, technical, and quality context package before generating test cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may cause the skill to activate during general analysis or requirements discussions. <br>
Mitigation: Review auto-invocation settings and use the skill when the workflow is ready to build a QA context package. <br>
Risk: The skill can read provided requirement documents or fetch supplied URLs, which may expose sensitive project context if used unintentionally. <br>
Mitigation: Provide only documents and links intended for QA analysis, and avoid private requirement materials or internal URLs unless they should be analyzed. <br>


## Reference(s): <br>
- [Output Template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown context package] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured sections for business context, user roles, functional boundaries, risks, assumptions, and QA output requirements.] <br>

## Skill Version(s): <br>
1.5.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
