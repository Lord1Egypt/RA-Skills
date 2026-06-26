## Description: <br>
Set up a PostHog metrics plan with an event funnel, KPI benchmarks, and kill/iterate/scale decision thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and product builders use this skill to create a project-specific PostHog metrics plan, including funnel events, KPI thresholds, implementation snippets, and decision rules for product iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project documentation to infer product context and analytics needs. <br>
Mitigation: Run it only in repositories where project documentation can be shared with the agent. <br>
Risk: The skill writes docs/metrics-plan.md and may overwrite or change an existing plan. <br>
Mitigation: Review the generated file or diff before accepting the change, especially when docs/metrics-plan.md already exists. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown document with tables, checklist-style decision rules, and Swift or TypeScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes docs/metrics-plan.md and summarizes the North Star metric, key thresholds, and first event to implement.] <br>

## Skill Version(s): <br>
1.1.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
