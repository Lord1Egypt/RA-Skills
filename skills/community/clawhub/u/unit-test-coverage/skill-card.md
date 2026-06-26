## Description: <br>
Unit test engineer skill for PHPUnit or Pest coverage, service-level assertions, and focused regression protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or update focused PHPUnit or Pest unit tests for WelineFramework services, helpers, models, and related logic. It helps produce deterministic regression coverage and reports the focused test command used for validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad coverage request could lead the agent to create tests that are not actually focused on unit-level behavior. <br>
Mitigation: Review the generated test scope, assertions, and reported command to confirm the work protects the intended unit-level regression. <br>
Risk: Small implementation changes made for testability could affect behavior outside the targeted unit boundary. <br>
Mitigation: Review generated diffs and run the focused PHPUnit or Pest command before accepting the changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/unit-test-coverage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with code changes, focused test commands, and validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should stay focused on unit-level behavior and include the protected regression case.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
