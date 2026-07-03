## Description: <br>
Validates generated test cases before final output by checking factual grounding, consistency, executability, and traceability against the provided requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and agents use this skill as a final guard before publishing generated test cases. It returns pass/fail validation with fact-check, consistency, executability, issue-list, and traceability findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad quality-check requests may activate this skill when a different review was intended. <br>
Mitigation: Confirm that the task is final test-case validation against requirements before applying its findings. <br>
Risk: Validation quality depends on the supplied requirements decomposition and generated test cases. <br>
Mitigation: Return unresolved or missing-source items in the issue list and require correction before final output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown validation report with pass/fail status, tables, issue lists, and traceability notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only QA checklist; expected inputs include generated test cases and a requirements decomposition table.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
