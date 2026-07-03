## Description: <br>
Helps QA reviewers compensate for common AI-generated test-case blind spots by expanding coverage across sequencing, concurrency, resource contention, state accumulation, data consistency, and third-party integration risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test leads, and developers use this skill after reviewing AI-generated test cases to identify missed scenarios and add supplemental blindspot coverage. It focuses on six recurring gaps: operation sequencing, concurrent use, resource exhaustion, long-running state, distributed data consistency, and real third-party integration behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad coverage-review prompts and produce many supplemental test cases. <br>
Mitigation: Use it when expanded QA blindspot planning is desired, then review generated cases for relevance, feasibility, and duplication before adding them to the test plan. <br>


## Reference(s): <br>
- [Six Blindspot Details](references/blindspot-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with coverage tables and supplemental test-case lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces blindspot IDs, links supplemental cases to requirement and original test-case IDs, and includes risk, difficulty, and suggested test-depth labels.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
