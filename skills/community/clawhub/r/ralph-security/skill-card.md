## Description: <br>
Comprehensive security audit with 100 iterations, covering OWASP Top 10, authentication, secrets, infrastructure, and code quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorukardahan](https://clawhub.ai/user/dorukardahan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to run a structured 100-iteration security audit of a project before releases, during onboarding, or as a recurring security check. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit inspects local project files and may surface sensitive paths, variable names, or secret indicators in its findings. <br>
Mitigation: Review and redact generated audit output before sharing it outside the project team. <br>
Risk: The skill writes and renames local Ralph report files during execution. <br>
Mitigation: Run it in the intended project workspace and review report file changes before committing or publishing them. <br>
Risk: Security findings may be inconclusive or pattern-based rather than verified vulnerabilities. <br>
Mitigation: Use the reported confidence and severity levels to prioritize manual verification before treating a finding as confirmed. <br>


## Reference(s): <br>
- [Severity definitions and triage guidance](references/severity-guide.md) <br>
- [Ralph Security Audit on ClawHub](https://clawhub.ai/dorukardahan/ralph-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown progress entries and a local Markdown audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or renames .ralph-report.md during execution and autosaves every 10 iterations.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
