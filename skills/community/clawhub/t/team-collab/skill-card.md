## Description: <br>
Team Collab organizes AI model roles into software development, monetization, and novel/comic-drama teams, using fixed role windows and model assignments for collaborative project work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business operators use Team Collab to route projects through predefined AI roles for requirements, implementation, testing, review, market analysis, content planning, and monetization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Role windows may retain context across discussions. <br>
Mitigation: Avoid sharing secrets or sensitive data, and use separate or cleared sessions for confidential work. <br>
Risk: Broad natural-language triggers may route a request into a multi-role workflow unexpectedly. <br>
Mitigation: Invoke teams with explicit wording and confirm the selected role or team before acting on outputs. <br>
Risk: The included project-start script creates folders and starter files in the current working directory. <br>
Mitigation: Run the script only in a new intended folder and review generated files before use. <br>
Risk: Helper files contain older version signals than the server release and SKILL.md. <br>
Mitigation: Treat the server release and SKILL.md version 3.1.0 as authoritative, and review helper scripts before operational use. <br>


## Reference(s): <br>
- [Team Collab ClawHub Page](https://clawhub.ai/davidme6/team-collab) <br>
- [Configuration Guide](config/README.md) <br>
- [Model Profiles](references/model-profiles.md) <br>
- [Project Collaboration Template](references/project-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and text with code blocks, command examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project folders and starter files when the included start-project script is run.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release and SKILL.md frontmatter; package.json reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
