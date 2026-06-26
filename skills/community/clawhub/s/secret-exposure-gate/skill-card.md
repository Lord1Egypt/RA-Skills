## Description: <br>
Checks a directory before release for possible secrets, tokens, private URLs, certificate fragments, or credential files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and skill publishers use this skill as a local pre-release gate to scan a chosen project or release directory for high-risk secret patterns and produce reviewable remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads a chosen local path and generated reports may include sensitive snippets or private URLs. <br>
Mitigation: Point it only at the intended project or release directory, keep reports private, and redact findings before sharing. <br>
Risk: Providing an output path writes the generated report to disk. <br>
Mitigation: Use stdout or dry-run behavior when a persistent report file is not desired, and review the output location before writing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/secret-exposure-gate) <br>
- [README](artifact/README.md) <br>
- [Output Specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a report file when an output path is provided; otherwise prints to stdout or supports dry-run behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
