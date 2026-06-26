## Description: <br>
WBS Planner helps agents organize project work into a Roadmap, Epic, and Task hierarchy with templates and task granularity standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ycz87](https://clawhub.ai/user/ycz87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Product managers, developers, and agent teams use this skill to plan project work, create roadmap, epic, and task files, and review task granularity before dispatching work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated roadmap, epic, or task text can misstate scope or acceptance criteria. <br>
Mitigation: Review planning files and acceptance criteria before assigning work to agents or developers. <br>
Risk: The Dev workflow can lead an agent to edit project files or run local build, test, and coding commands. <br>
Mitigation: Install only in trusted projects and review file changes and commands according to local policy. <br>
Risk: Task text from untrusted sources can carry misleading planning guidance into downstream work. <br>
Mitigation: Validate or rewrite externally supplied task descriptions before dispatching them. <br>


## Reference(s): <br>
- [Task Breakdown Guide](references/breakdown-guide.md) <br>
- [PM Workflow](references/pm-workflow.md) <br>
- [Dev Workflow](references/dev-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance, Shell commands] <br>
**Output Format:** [Markdown planning documents and concise workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update roadmap, epic, and task Markdown files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
