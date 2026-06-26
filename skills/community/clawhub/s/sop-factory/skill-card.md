## Description: <br>
Turn rough workflows into standard operating procedures with roles, inputs, outputs, checkpoints, and exception handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and process owners use this skill to turn rough workflow notes into draft SOPs, quick-start versions, roles matrices, and exception appendices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft SOPs may be incomplete, incorrect, or unsuitable as official procedure without review. <br>
Mitigation: Review generated SOP drafts before treating them as authoritative and keep assumptions explicit. <br>
Risk: The helper script writes an output file and may overwrite a path the user provides. <br>
Mitigation: Run the helper only with an output filename that is acceptable to create or overwrite. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/sop-factory) <br>
- [SOP template resource](artifact/resources/sop_template.md) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown drafts and structured SOP outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local Python helper to create a JSON SOP outline file when the user asks for a structured file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
