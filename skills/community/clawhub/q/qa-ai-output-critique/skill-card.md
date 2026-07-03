## Description: <br>
Reviews AI-generated test cases across quality dimensions including completeness, correctness, executability, risk coverage, formatting, traceability, consistency, and redundancy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and test reviewers use this skill after an agent generates test cases to check whether the cases are useful, executable, risk-aware, and ready to improve before final delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scoring guidance may be inconsistent across the six-dimension and eight-dimension review language. <br>
Mitigation: Review the generated scorecard before relying on pass or fail decisions, and align the active rubric with the intended review mode. <br>
Risk: A review can be less complete when scenario trees, risk lists, or requirement IDs are not provided. <br>
Mitigation: Provide scenario, risk, and traceability inputs for full reviews, or treat downgrade notes as limits on the report's completeness. <br>
Risk: The skill may critique generated test cases automatically before final output. <br>
Mitigation: Inspect the final critique and improvement suggestions before applying changes to a test suite. <br>


## Reference(s): <br>
- [Report Templates](references/report-templates.md) <br>
- [Review Dimensions](references/review-dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review report with scores, issue lists, coverage gaps, and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a full review when scenario and risk inputs are present, or a simplified review with downgrade notes when optional inputs are missing.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
