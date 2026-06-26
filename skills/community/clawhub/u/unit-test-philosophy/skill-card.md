## Description: <br>
Provides risk-based unit testing and Allure-readable behavioral spec guidance for open-agreements repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adding tests, expanding coverage, or reviewing test quality in open-agreements codebases. It emphasizes behavior-oriented assertions, Allure-readable Given/When/Then steps, and OpenSpec traceability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Listed npm commands may be inappropriate for a repository or workspace if run without review. <br>
Mitigation: Confirm each command fits the local repository before allowing an agent to run it. <br>
Risk: Allure attachments can accidentally include credentials or private production data. <br>
Mitigation: Use sanitized fixtures and avoid adding secrets or private production data to test attachments. <br>
Risk: Testing guidance can still lead to misleading tests or incorrect spec traceability if applied mechanically. <br>
Mitigation: Review generated tests and spec mappings before deployment. <br>


## Reference(s): <br>
- [Allure Test Spec Writing Guide](references/allure-test-spec-writing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with inline TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides documentation-only recommendations; it does not execute commands or modify code by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
