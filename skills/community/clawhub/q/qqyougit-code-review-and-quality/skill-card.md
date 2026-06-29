## Description: <br>
Provides multidimensional code and plan review guidance covering correctness, readability, architecture, security, performance, and agent-skill security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill before merging changes, after feature work or bug fixes, and when evaluating code or technical plans produced by agents or models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill as an automatic gate for every small task can create unnecessary review friction. <br>
Mitigation: Install it as a general review aid and invoke it when a code or change review is actually needed. <br>
Risk: Review prompts may expose sensitive repository context. <br>
Mitigation: Avoid feeding sensitive repository context unless review is needed. <br>
Risk: Broad review guidance can produce findings that require scope clarification or human judgment. <br>
Mitigation: Review and scan the skill before deployment, and have maintainers confirm findings before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/qqyougit-code-review-and-quality) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown review guidance with checklists, severity-labeled findings, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approval or request-changes recommendations plus verification steps.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
