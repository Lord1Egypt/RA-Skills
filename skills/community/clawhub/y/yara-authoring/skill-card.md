## Description: <br>
Write high-quality YARA-X detection rules for malware hunting, with guidance on atom selection, string optimization, false positive reduction, module usage, rule templates, and testing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, malware researchers, and detection engineers use this skill to draft, review, optimize, and test YARA-X rules for malware hunting while reducing false positives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or revised detection rules can create false positives or miss targeted malware behavior. <br>
Mitigation: Review rule logic, require multiple specific indicators, and test against representative malware and goodware corpora before deployment. <br>
Risk: YARA-X commands or proposed rule changes may affect local files or operational detection workflows if used without review. <br>
Mitigation: Run validation and scans in a controlled environment, inspect commands before execution, and format or check rules with YARA-X tooling before publishing. <br>
Risk: Server security evidence reports a clean verdict but notes that full artifact coherence verification was unavailable. <br>
Mitigation: Review the skill artifact and any install requirements before installing, paying attention to credential requests, broad file access, background behavior, or external account changes. <br>


## Reference(s): <br>
- [Yara Authoring Skill Page](https://clawhub.ai/solomonneas/yara-authoring) <br>
- [Trail of Bits YARA Authoring Methodology](https://github.com/trailofbits/skills/tree/main/plugins/yara-authoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with YARA code examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed rule authoring guidance rather than executing scans directly.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
