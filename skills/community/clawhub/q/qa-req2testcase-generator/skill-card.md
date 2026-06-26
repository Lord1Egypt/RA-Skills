## Description: <br>
AI-driven Chinese requirement analysis and test-case generation workflow using an orchestrated, staged process for PRD review, feature decomposition, test-point drafting, risk and PCI identification, and final test-case export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loveshaozhe](https://clawhub.ai/user/loveshaozhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers and delivery teams use this skill to convert Chinese requirement documents or pasted requirement text into structured analysis, feature trees, test points, risk notes, and detailed executable test cases. It is aimed at financial-services testing workflows where domain knowledge, review gates, and Excel or Markdown handoff are important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement-derived content may be uploaded to an external review service by default. <br>
Mitigation: Disable or remove the bundled cloud review configuration before processing confidential or regulated documents. <br>
Risk: Bundled configuration includes hardcoded review-service credentials and non-HTTPS endpoints. <br>
Mitigation: Remove hardcoded API keys, provide credentials through a managed secret channel, and require HTTPS endpoints before installation. <br>
Risk: Broad local discovery and credential persistence can expose files or shared passwords beyond the intended task. <br>
Mitigation: Provide explicit input file paths, restrict accessible work directories, and avoid entering shared passwords through chat until credential storage behavior has been fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loveshaozhe/qa-req2testcase-generator) <br>
- [Onboarding instructions](references/onboarding.md) <br>
- [Orchestrator protocol](references/orchestrator_protocol.md) <br>
- [Test case design standard](knowledge/company_standards/testcase_design_spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [Chinese-language status messages, structured JSON intermediates, Markdown summaries, and Excel or Markdown export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses staged quality gates and local artifact files; image understanding and cloud review behavior depend on bundled configuration.] <br>

## Skill Version(s): <br>
4.12.6 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
