## Description: <br>
Complete testing workflow from requirements analysis to test case generation and review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garkinchu](https://clawhub.ai/user/garkinchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test engineers, and developers use this skill to run a structured testing workflow across requirements analysis, design review, test case generation, and test case review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is tagged as requiring OAuth-token access, but the artifact documentation does not explain why that access is needed. <br>
Mitigation: Confirm the OAuth-token requirement before installation and grant only the minimum permissions needed. <br>
Risk: The test case generation workflow can create or overwrite CSV files. <br>
Mitigation: Keep outputs in a chosen workspace folder and confirm the target file path before allowing CSV creation or overwrite. <br>


## Reference(s): <br>
- [Tester Workflow README](README.md) <br>
- [Workflow Guide](reference/workflow-guide.md) <br>
- [Full Workflow Example](examples/full-workflow.md) <br>
- [Requirement Analysis Checklist](included-skills/analyze-requirements/reference/checklist.md) <br>
- [Design Understanding Checklist](included-skills/understand-design/reference/8-dimensions-checklist.md) <br>
- [Test Case Generation Process](included-skills/generate-test-cases/reference/generation-process.md) <br>
- [Test Case Format Specification](included-skills/generate-test-cases/reference/format-spec.md) <br>
- [Test Case Review Checklist](included-skills/review-test-cases/reference/review-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/garkinchu/tester-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown reports, prioritized issue lists, and CSV test case files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated CSV test case files use UTF-8 BOM encoding and a double-pipe delimiter when the test case generation sub-skill is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
