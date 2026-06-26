## Description: <br>
Generates high-quality positive, negative, and edge-case examples for skills to improve routing and understandability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to draft reviewable positive examples, negative examples, edge cases, common misfires, placement guidance, and maintenance notes for skill documentation and release preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional helper can read a selected input path and include that content in generated drafts. <br>
Mitigation: Point it only at files or directories intended for the draft, and redact sensitive or personal information before use. <br>
Risk: The optional helper can write to a selected output file. <br>
Mitigation: Use stdout or dry-run mode for review first, and choose an explicit non-sensitive output path when writing a file. <br>
Risk: Generated examples may be too generic or may omit important non-trigger cases if the input brief is thin. <br>
Mitigation: Review the draft against the skill's routing boundaries and add missing positive, negative, and edge-case examples before release. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/52YuanChangXing/skill-example-synthesizer) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](artifact/README.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional Python helper can read a user-selected input file or directory and can write to a user-selected output path; dry-run and stdout modes are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
