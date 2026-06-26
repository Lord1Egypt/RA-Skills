## Description: <br>
Test-driven development with red-green-refactor loop and de-sloppify pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to build features and fix bugs with a test-first workflow focused on public behavior, integration-style tests, incremental red-green cycles, and a cleanup pass that removes low-value test or code slop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional examples include broad cleanup, verification, and commit workflows that could change a repository if followed without review. <br>
Mitigation: Ask before broad code changes or commits, review the working tree after cleanup, and run the relevant build, lint, and test suite before accepting changes. <br>
Risk: A cleanup pass can remove useful tests or validations if business-critical behavior is misclassified as low-value coverage. <br>
Mitigation: Keep tests that cover business logic, integration behavior, real edge cases, and security validations; remove only redundant language, framework, or duplicate coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huamu668/tdd-ecc) <br>
- [Good and Bad Tests](artifact/tests.md) <br>
- [When to Mock](artifact/mocking.md) <br>
- [Interface Design for Testability](artifact/interface-design.md) <br>
- [Deep Modules](artifact/deep-modules.md) <br>
- [Refactor Candidates](artifact/refactoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces test plans, implementation guidance, refactoring guidance, and cleanup checklists through normal agent text output.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
