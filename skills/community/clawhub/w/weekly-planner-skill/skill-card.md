## Description: <br>
工作日日报与周记录整理工具，自动生成工作日报，梳理计划、完成、反思；当用户需要生成工作日报、管理周记录或查看总结时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual contributors use this skill to record plans, completions, and reflections, then generate daily work reports and weekly summaries. It helps an agent organize local weekly planner data, query progress by day or category, and produce concise planning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planner entries, completion notes, and reflections are stored locally in ./weekly-plans JSON files and may contain sensitive work context. <br>
Mitigation: Avoid recording secrets or highly sensitive reflections, and review local planner files before sharing or committing the workspace. <br>
Risk: Deleting a plan uses a soft-delete behavior, so some deleted task data may remain in the weekly JSON file. <br>
Mitigation: Manually remove sensitive deleted entries from the JSON file when permanent removal is required. <br>


## Reference(s): <br>
- [Data Format](references/data-format.md) <br>
- [Query Templates](references/query-templates.md) <br>
- [Daily Report Template](references/daily-report-template.md) <br>
- [Weekly Report Template](references/weekly-report-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ludiansheng/weekly-planner-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/ludiansheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summaries and JSON-backed planner records with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores planner data in local ./weekly-plans JSON files] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
