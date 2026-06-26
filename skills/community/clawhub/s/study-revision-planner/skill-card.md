## Description: <br>
Convert a syllabus, exam scope, or course notes into a revision calendar with spaced review, mock tests, and weak-point loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and learners use this skill to convert course material and exam scope into a practical revision plan with study blocks, spaced reviews, mock tests, and weak-topic follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python helper writes CSV output and could replace an important file if the chosen output path already exists. <br>
Mitigation: Use an explicit noncritical output filename and review the target path before running the helper. <br>
Risk: Server evidence notes a small provenance/version mismatch. <br>
Mitigation: Review the server release version against the artifact frontmatter and changelog before relying on version-specific claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/study-revision-planner) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Artifact README](artifact/README.md) <br>
- [Example prompt](artifact/examples/example-prompt.md) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, tables, checklists, and optional CSV output from the local Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on user-provided syllabus, topic difficulty, exam date, weekly availability, and preferred study block length.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
