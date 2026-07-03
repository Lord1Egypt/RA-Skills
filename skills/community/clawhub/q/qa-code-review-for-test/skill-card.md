## Description: <br>
Analyzes code changes from a testing perspective to identify impact scope, high-risk patterns, test gaps, and a minimal regression testing scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and reviewers use this skill when a pull request or code diff needs test-focused impact analysis. It helps identify affected areas, missing tests, risk patterns, and regression coverage without performing a full code-quality review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad code-review wording and produce guidance that is too general for the specific change. <br>
Mitigation: Use clear prompts that include the code diff, related test cases, and the desired testing perspective, then review the generated recommendations before applying them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown report with structured review findings, test gaps, impact analysis, and regression scope] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a code diff or change description and related test cases; a requirements document is optional.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
