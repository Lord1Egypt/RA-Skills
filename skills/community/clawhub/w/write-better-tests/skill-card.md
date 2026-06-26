## Description: <br>
Use when Codex is adding, editing, selecting, reviewing, or explaining tests in any repository, including mocks, fixtures, snapshots, CI validation, regression coverage, TDD/red-green proof, or readiness claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to design, revise, review, and report on behavior-first tests that prove real regressions instead of only exercising implementation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Red-green proof work can involve temporary reverted or injected changes that should not remain in the final diff. <br>
Mitigation: Review the final diff, remove temporary proof changes, and rerun the focused validation before relying on the result. <br>


## Reference(s): <br>
- [Test Smell Reference](references/test-smells.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with inline code, test examples, and command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend focused test runs, red-green proof steps, and final validation reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
