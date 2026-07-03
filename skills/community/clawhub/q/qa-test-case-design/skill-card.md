## Description: <br>
Designs structured, traceable QA test cases from completed requirement, scenario, boundary, and combination analysis, with P0-P3 prioritization and standardized test-case fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and product teams use this skill to turn requirement context into structured test-case reports with priorities, traceability IDs, coverage notes, and review-ready expected results. It is intended for use after upstream analysis is complete, not as a replacement for requirement clarification or human test execution planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include secrets or unrelated private data when providing requirement context. <br>
Mitigation: Provide only the requirements and business context needed for test design, and avoid pasting credentials, secrets, or unrelated private data. <br>
Risk: Generated test cases can be incomplete or generic when requirement, scenario, boundary, or combination analysis is missing. <br>
Mitigation: Use the skill after upstream analysis is complete, supply clear requirements and constraints, and review the output for missing scenarios before relying on it. <br>
Risk: The skill does not inspect implementation code and may not capture system-specific execution details. <br>
Mitigation: Use the output as requirement-based test design guidance, then have testers complete execution steps and validate expected results against the actual system. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kokxi/skills/qa-test-case-design) <br>
- [Design methods reference](references/design-methods.md) <br>
- [Coverage and quality reference](references/coverage-and-quality.md) <br>
- [Review standards reference](references/review-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown test-case reports and tables with traceability fields, priority groupings, coverage analysis, and test guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Test steps are intentionally left for users to complete against the actual system.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
