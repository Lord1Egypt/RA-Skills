## Description: <br>
Skill Dashboard helps users list, page through, inspect, update, uninstall, enable, and disable installed ClawHub skills from an agent conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to review installed skills, open ClawHub skill pages, check skill status, and perform common skill-management actions with confirmation prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence says update and uninstall paths can turn a skill name into a local shell command. <br>
Mitigation: Validate skill slugs with a strict allowlist and use execFile or spawn with argument arrays before installing or publishing this version. <br>
Risk: Update and uninstall actions can change or remove local skills. <br>
Mitigation: Keep clear user confirmation prompts before execution and review the selected skill name before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/largetool/skill-dashboard) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Conversational text and Markdown reports with concise command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local skill state cache files and may call the local clawhub CLI for list, inspect, update, and uninstall actions.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
