## Description: <br>
JSON-driven browser form automation for AI agents, supporting form filling, conditional branching, structured extraction, and PII redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duz1287](https://clawhub.ai/user/duz1287) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to automate browser-based form workflows, including data entry, form submission, file upload, conditional page interaction, and structured extraction from resulting pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated browser steps can submit forms, create accounts, log in, or perform other user-visible actions. <br>
Mitigation: Require a clear consent statement and review each generated run before execution, especially submit, registration, and login flows. <br>
Risk: File uploads, extracted page content, screenshots, traces, and debug artifacts may expose sensitive data. <br>
Mitigation: Keep PII redaction enabled, avoid unnecessary debug output, and inspect upload and extraction targets before running. <br>
Risk: Disabling browser sandboxing or running against untrusted pages increases exposure to malicious web content. <br>
Mitigation: Keep sandbox mode enabled except for trusted local test environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/duz1287/web-auto-form) <br>
- [Project Homepage](https://github.com/DUZ1287/WebAutoForm) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON configuration, JSON execution results, Markdown guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution results may include status, step outcomes, extracted fields, screenshots, debug artifact paths, and error details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
