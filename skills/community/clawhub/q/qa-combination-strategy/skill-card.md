## Description: <br>
Helps QA teams reduce combination-test explosion by using pairwise coverage, orthogonal testing, decision-table thinking, and risk-weighted combinations to produce coverage matrices and identify gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test designers, and developers use this skill to turn scenario trees, requirement breakdowns, and optional risk assessments into efficient combination-test plans. It is most useful when full combinatorial coverage is impractical across many parameters, environments, or dependent input values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reduced combination sets may miss critical interactions in high-risk workflows. <br>
Mitigation: Manually review generated matrices and add full coverage for high-risk, safety-sensitive, payment, security, or complex dependency flows. <br>
Risk: Broad QA terminology may trigger the skill when pairwise or orthogonal reduction is not the right strategy. <br>
Mitigation: Confirm the parameters, value ranges, business rules, and risk levels before relying on a reduced matrix. <br>
Risk: The skill produces QA planning guidance rather than executable tests. <br>
Mitigation: Convert the matrix into concrete test cases with clear preconditions, steps, and expected results before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-combination-strategy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown with combination matrices, pairwise combinations, N-way analysis, and coverage-gap notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before being converted into executable test cases, especially for high-risk flows.] <br>

## Skill Version(s): <br>
1.5.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
