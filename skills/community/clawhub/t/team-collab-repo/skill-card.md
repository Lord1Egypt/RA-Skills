## Description: <br>
Team Collab Repo coordinates an agent workflow where product, development, design, testing, review, legal, art, and market-analysis roles collaborate on project planning and delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to structure multi-role agent collaboration for building applications, writing complex code, planning projects, and reviewing outputs across product, engineering, design, testing, compliance, art, and market-analysis roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad team-collaboration phrasing may trigger the workflow when the user intended ordinary planning help. <br>
Mitigation: Use explicit invocation wording and confirm that the multi-role workflow is desired before applying it. <br>
Risk: Advanced model-switching can involve multiple model sessions and additional cost. <br>
Mitigation: Review the workflow before use and choose the lower-cost role-play mode unless separate model sessions are needed. <br>
Risk: The project initialization script creates a new project folder and template files in the current working directory. <br>
Mitigation: Run it only from a directory where creating a new project folder is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidme6/team-collab-repo) <br>
- [Model Profiles](artifact/references/model-profiles.md) <br>
- [Project Collaboration Template](artifact/references/project-template.md) <br>
- [Role Configuration Guide](artifact/config/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional code blocks, shell command examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project folders and project.json or README.md templates when the initialization script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
