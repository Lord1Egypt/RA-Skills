## Description: <br>
A requirement gate checker for requirement completeness, acceptance criteria, and scope validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terr123123](https://clawhub.ai/user/terr123123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, product managers, and reviewers use this skill before design or development to check whether requirements are complete, testable, measurable, and clearly scoped. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement content may contain sensitive project details. <br>
Mitigation: Run the checker in the approved local development environment and handle requirement inputs as project data. <br>
Risk: Gate results may be treated as a final product decision even though they are quality signals. <br>
Mitigation: Use the results to support human requirement review before blocking or approving design and development work. <br>
Risk: Included tests create temporary JSON files during normal validation. <br>
Mitigation: Run tests only in a normal development environment where temporary test files are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terr123123/skills/requirement-gate) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Guidance] <br>
**Output Format:** [Python objects with human-readable messages and JSON-serializable dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns GateResult records with pass/fail status, scores, messages, and details for completeness, acceptance criteria, and scope checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
