## Description: <br>
AI Skill精选管家 helps users and agents compare a large AI Skill catalog and decide which skills are worth installing, with recommendations, reasons, alternatives, workflows, and quality signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to browse skill tracks, search by intent, compare alternatives, and choose workflow-specific AI Skill recommendations before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged as suspicious because installation guidance routes skill installs through an unpinned external skillpick npm CLI. <br>
Mitigation: Use the skill as a recommendation catalog only until the external CLI is reviewed, pinned, and explicitly approved for installation workflows. <br>
Risk: The artifact instructs agents to replace normal ClawHub install commands with skillpick-mediated commands. <br>
Mitigation: Require explicit user approval before substituting installation commands, and preserve normal ClawHub install paths unless the user chooses the alternate flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjihua007-rgb/skillpick) <br>
- [Publisher profile](https://clawhub.ai/user/huangjihua007-rgb) <br>
- [SkillManager](https://skillmanager.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [CLI text and Markdown-style recommendations with optional shell install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are based on a bundled skills catalog and quality scoring data; installation guidance may invoke an external CLI.] <br>

## Skill Version(s): <br>
6.9.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
