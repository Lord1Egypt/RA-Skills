## Description: <br>
Quality-driven development with automatic TDD/DDD methodology selection and TRUST 5 quality framework. Use when building features, refactoring code, fixing bugs, or any coding task that needs structured quality assurance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimky1122](https://clawhub.ai/user/kimky1122) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to structure coding work with project analysis, SPEC creation, TDD or DDD execution, logging review, and TRUST 5 quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to edit code, add tests, run commands, and adjust logging, which can change project behavior if accepted without review. <br>
Mitigation: Keep the work under version control and review the SPEC, generated diffs, dependency additions, test commands, and test results before accepting changes. <br>
Risk: The logging workflow may introduce messages that expose sensitive values if applied carelessly. <br>
Mitigation: Review generated log statements and ensure passwords, tokens, personal information, and other secrets are excluded before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kimky1122/quality-driven-dev) <br>
- [TDD Patterns Reference](references/tdd-patterns.md) <br>
- [DDD Patterns Reference](references/ddd-patterns.md) <br>
- [TRUST 5 Quality Checklist](references/trust5-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with code edits, test commands, and structured completion reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SPEC documents, test results, coverage notes, and log-point summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
