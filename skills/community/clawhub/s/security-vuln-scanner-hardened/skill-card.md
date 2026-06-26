## Description: <br>
Scan source code for security vulnerabilities and suggest fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review source code for common security vulnerabilities, receive severity-oriented findings, and get focused remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan reports can expose secrets, vulnerable file paths, line numbers, or exploit-relevant code details. <br>
Mitigation: Treat scan inputs and outputs as sensitive, redact actual secret values, and keep findings within the conversation or approved internal workflows. <br>
Risk: Bundling unrelated refactors with a vulnerability fix can introduce regressions in untested code paths. <br>
Mitigation: Apply focused security fixes only and handle broader cleanup as separate follow-up work. <br>
Risk: Broad trigger wording could activate the skill when a narrower security review was not intended. <br>
Mitigation: Invoke the skill with explicit scope such as 'scan this code for vulnerabilities' and confirm large or ambiguous scan requests before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/security-vuln-scanner-hardened) <br>
- [Publisher Profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/security-vuln-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-style vulnerability summaries and code examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should redact actual secrets, keep security fixes narrowly scoped, and avoid sending scan results or findings to external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
