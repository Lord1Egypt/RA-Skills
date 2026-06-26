## Description: <br>
问卷网 helps agents create, edit, publish, stop, report on, and export data from Wenjuan survey, form, vote, and assessment projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenjuanwang](https://clawhub.ai/user/wenjuanwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate Wenjuan projects, including creating and publishing questionnaires, managing questions and project metadata, viewing reports, and exporting response data. It is intended for accounts where the user has authority to manage the corresponding Wenjuan surveys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use saved account credentials to publish, stop, edit, delete, and export survey data. <br>
Mitigation: Install only for Wenjuan accounts the user is authorized to operate, review each high-impact action before execution, and keep local credential directories private. <br>
Risk: Several high-impact actions rely on documented user confirmation rather than built-in confirmation gates. <br>
Mitigation: Require explicit user approval before publishing, stopping collection, editing, deleting questions, or exporting response data. <br>
Risk: Local tokens or exported survey data could be exposed if committed or shared. <br>
Mitigation: Do not commit token files or exports, and keep ~/.wenjuan and the skill .wenjuan directory out of shared artifacts. <br>
Risk: The setup script can install Node.js dependencies or tooling on the host. <br>
Mitigation: Prefer installing Node.js and dependencies through the user's normal trusted system package workflow before running the skill setup script. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenjuanwang/wenjuan-survey) <br>
- [Wenjuan Homepage](https://www.wenjuan.com) <br>
- [README](README.md) <br>
- [Skill Overview](references/skill_overview.md) <br>
- [Create Survey](references/create_survey.md) <br>
- [Authentication](references/auth.md) <br>
- [Export Data](references/export_data.md) <br>
- [Project JSON Structure Guide](references/project_json_structure_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and script output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, modify, publish, stop, delete, report on, or export Wenjuan survey data when the user authorizes the requested action.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
