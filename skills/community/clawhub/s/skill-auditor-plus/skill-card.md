## Description: <br>
Security, performance, and quality auditing for AgentSkills, including checks for dangerous operations, credential leaks, token bloat, and quality issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caleb-niu007](https://clawhub.ai/user/caleb-niu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review AgentSkills before installation or during development by running audits for security risks, token and performance issues, and quality best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit scripts inspect local skill files and may include file paths, matched text, and context snippets in their reports. <br>
Mitigation: Run audits only on intended skill directories and review generated reports before sharing them outside the working environment. <br>
Risk: The security scanner is pattern-based and can produce false positives or miss risks that are outside its rules. <br>
Mitigation: Use the findings as review prompts, then manually inspect high-impact behavior before installing or publishing a skill. <br>
Risk: The release is tagged with a sensitive-credentials capability, but the server security guidance says not to grant credentials unless clearly needed. <br>
Mitigation: Avoid granting credentials, broad file access, or mutation authority unless the specific audit task requires those permissions. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/caleb-niu007/skill-auditor-plus) <br>
- [AgentSkill best practices](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON audit report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces severity-ranked findings, metrics, and remediation guidance for local skill directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
