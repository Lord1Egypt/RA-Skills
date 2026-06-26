## Description: <br>
Design helps agents create customized design-project skills and supporting references that guide users from requirements definition through research, solution design, review, and delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balancegsr](https://clawhub.ai/user/balancegsr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a tailored design-project skill for product, interaction, experience, information architecture, visual, or related design work. The generated project skill helps structure intake, research, design decisions, review, delivery, and project memory across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and installs design-project skills with local project files that future sessions may reload as project memory. <br>
Mitigation: Install only in a workspace where generated design files are acceptable, review the preview and delivery mode before confirming, and avoid placing unrelated secrets or private material in project files. <br>
Risk: The artifact declares local write and bash capabilities for creating generated skill and project folder structures. <br>
Mitigation: Confirm the generated paths and delivery choice before file creation, and review generated content before using it in sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/balancegsr/skill-creator-design) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Review Checklist Template](artifact/references/templates/guides/review_checklist.md) <br>
- [Full Summary Guide Template](artifact/references/templates/guides/summary_guide_full.md) <br>
- [Lite Summary Guide Template](artifact/references/templates/guides/summary_guide_lite.md) <br>
- [Full Skill Template](artifact/references/templates/skill/full.md) <br>
- [Lite Skill Template](artifact/references/templates/skill/lite.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill files, reference files, project folders, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can install generated skill files into the current workspace or package them as a ZIP after user confirmation.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
