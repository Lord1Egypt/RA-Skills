## Description: <br>
Provides QA heuristic checklists for common feature types such as forms, lists, carts, payments, import/export, approvals, notifications, and permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, testers, and product teams use this skill to identify a feature type and produce practical testing checklists for new or unfamiliar functionality. It is especially useful when a tester needs a structured starting point for common high-risk areas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be invoked for broad testing requests where a functional checklist is too general for the user's actual need. <br>
Mitigation: Confirm the target feature type and use specialized security, performance, or debugging skills when those domains are the primary concern. <br>
Risk: Checklist output can omit product-specific business rules, historical defects, or environment constraints. <br>
Mitigation: Supplement the generated checklist with project-specific requirements, known defect patterns, and reviewer judgment before relying on it for release coverage. <br>


## Reference(s): <br>
- [Functional heuristic checklists](references/checklists.md) <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-heuristic-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include covered areas, uncovered areas, and exploration guidance based on the requested testing context.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
