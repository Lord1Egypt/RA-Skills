## Description: <br>
Scan OpenClaw skill directories for high-signal security risks such as download-and-execute chains, obfuscated execution, and suspicious callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan OpenClaw skill directories before installation, publishing, or CI release gates. It helps identify risky shell patterns, suspicious callbacks, obfuscated execution, and social-engineering instructions without executing the target skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan targets and findings may be exposed in command output or CI artifacts. <br>
Mitigation: Scan only directories whose contents are acceptable to expose in local logs or CI output. <br>
Risk: The package contains intentionally dangerous-looking fixture files used to test scanner behavior. <br>
Mitigation: Do not manually run files under fixtures/malicious-skill; treat them as test data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mike007jd/skill-sentinel) <br>
- [Publisher Profile](https://clawhub.ai/user/mike007jd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, plus JSON and SARIF scanner output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Scan results include a risk level, finding counts, rule IDs, file locations, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
