## Description: <br>
Conducts non-destructive client-side security assessments of web applications and produces a structured Markdown report covering browser-facing attack surface categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enderphan94](https://clawhub.ai/user/enderphan94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and authorized assessors use this skill to review the browser-facing attack surface of websites and web applications, including client-side vulnerabilities, exposed data, dependency risks, and security headers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a client-side security assessment against an unauthorized or wrong target can create legal, operational, or privacy risk. <br>
Mitigation: Confirm authorization, target URL, credentials, and client-side scope before use, and stay within the approved scope. <br>
Risk: Active or noisy scanning may affect the target service or exceed the intended assessment posture. <br>
Mitigation: Use passive analysis first, keep request volume moderate, and obtain explicit approval before active or noisy scanning. <br>
Risk: Saved reports may contain sensitive URLs, tokens, exposed endpoints, or vulnerability evidence. <br>
Mitigation: Treat generated reports and evidence as sensitive security material and share them only with authorized recipients. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security assessment report with findings, remediation, and appendix evidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The expected final report is client_side_pentest_report.md and may include commands, URLs, reproduction steps, and raw evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
