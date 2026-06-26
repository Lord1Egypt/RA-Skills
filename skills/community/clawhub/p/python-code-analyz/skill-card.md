## Description: <br>
Analyzes Python code for syntax, security, reliability, performance, and quality issues, then provides prioritized findings and directly usable improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sujian0606-cpu](https://clawhub.ai/user/sujian0606-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code-review agents use this skill to inspect Python files or pasted code, rank issues from P0 to P3, and obtain concrete remediation suggestions or refactored code. It is suited for local review workflows where generated fixes are inspected before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publisher is not verified by NVIDIA and server-resolved GitHub provenance is unavailable. <br>
Mitigation: Install only if you trust the ClawHub publisher handle, and treat placeholder source links as non-authoritative. <br>
Risk: Generated fixes or refactoring suggestions may alter behavior or introduce incorrect changes. <br>
Mitigation: Review generated code before applying it and run the project's normal tests or static checks after changes. <br>
Risk: The artifact includes a publishing helper that can publish to ClawHub if run deliberately. <br>
Mitigation: Do not run the publishing helper unless you intend to publish with your own ClawHub account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sujian0606-cpu/python-code-analyz) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text analysis reports with code blocks; JSON output is available for CLI use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are grouped by P0/P1/P2/P3 severity and may include line numbers, rule identifiers, suggestions, and generated replacement code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.yaml, package.json, CHANGELOG released 2026-03-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
