## Description: <br>
Manages a user's own QQ Zone photo albums, including login, album browsing, photo viewing, and single-photo downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage and back up their own QQ Zone photos through an agent workflow. It is intended for album browsing, photo inspection, and single-photo download, not batch download, album editing, or managing other people's photos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests exec and write access for QQ Zone photo operations. <br>
Mitigation: Review proposed commands before execution and grant only the minimum file and execution access needed for the current task. <br>
Risk: QQ cookies or login sessions could expose account access if handled carelessly. <br>
Mitigation: Use the skill only with the user's own QQ account, keep cookies private, avoid shared workspaces for credentials, and revoke or rotate sessions when finished. <br>
Risk: The artifact includes unrelated project-management routing text that does not match the QQ Zone photo use case. <br>
Mitigation: Treat only QQ Zone photo management as supported and ignore unrelated task-management language. <br>
Risk: The artifact refers to scripts and commands, but the provided artifact evidence contains only SKILL.md. <br>
Mitigation: Identify and inspect any scripts before running commands, and do not execute placeholder commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/qq-zone-photo-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded image files when the proposed commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
