## Description: <br>
Reviews requirement documents across completeness, clarity, consistency, testability, and feasibility before QA planning or test design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, product reviewers, and developers use this skill to assess PRDs or requirement descriptions before creating test plans or test cases. It produces a structured review with five-dimension scoring, issue severity, and improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be invoked for broader testing tasks that include requirements even when the user expected a narrower workflow. <br>
Mitigation: Call it explicitly when requirement-quality review is desired, or confirm scope before applying its findings to downstream QA planning. <br>
Risk: Requirement-review findings can affect test strategy and may overstate or miss issues in ambiguous source requirements. <br>
Mitigation: Have the product owner or QA lead review P0/P1 findings and clarify missing requirement details before test design proceeds. <br>


## Reference(s): <br>
- [Review Standards](references/review-standards.md) <br>
- [Report Template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown requirement review report with scoring, issue lists, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes completeness, clarity, consistency, testability, and feasibility scoring plus P0-P2 issue classification.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
