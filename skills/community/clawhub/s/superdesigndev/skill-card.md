## Description: <br>
Superdesign is a frontend UI/UX design agent for analyzing existing interfaces, preparing design-system context, and generating or iterating design drafts through the SuperDesign CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayZeeDesign](https://clawhub.ai/user/JayZeeDesign) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and designers use this skill before frontend implementation to collect UI source context, define or reuse design-system guidance, reproduce current pages, branch design variations, extract reusable components, and extend approved designs across flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan substantial frontend source and write persistent context files that may include sensitive or proprietary material. <br>
Mitigation: Approve exactly which files are included as context, exclude secrets, proprietary non-UI code, server logic, and sensitive configs, and review generated .superdesign files before reuse. <br>
Risk: The skill relies on mutable remote guideline files that can change independently of the released artifact. <br>
Mitigation: Review and pin the remote instruction files before execution when repeatability or policy control matters. <br>
Risk: The workflow can install or update a global npm CLI and requires account login before design commands run. <br>
Mitigation: Use an isolated environment, approve or pin the CLI version, and use an appropriate SuperDesign account with least-privilege project access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JayZeeDesign/superdesigndev) <br>
- [SuperDesign init guidelines](https://raw.githubusercontent.com/superdesigndev/superdesign-skill/main/skills/superdesign/INIT.md) <br>
- [SuperDesign workflow guidelines](https://raw.githubusercontent.com/superdesigndev/superdesign-skill/main/skills/superdesign/SUPERDESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated context files, and SuperDesign CLI design draft outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .superdesign/init/*.md, .superdesign/design-system.md, temporary component HTML, and design drafts through the SuperDesign CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
