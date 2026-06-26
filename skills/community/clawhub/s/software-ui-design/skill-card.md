## Description: <br>
Assists UI design workflows by parsing design files, generating annotations and reports, checking UI specifications, organizing design assets, and drafting design-to-code outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaochunz030-spec](https://clawhub.ai/user/xiaochunz030-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers and frontend developers use this skill to extract design information from Figma files and review UI reports against brand color, typography, and spacing rules before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Figma parsing uses a user-provided Personal Access Token and design file data. <br>
Mitigation: Use a dedicated or least-privileged Figma token where possible, avoid sharing it in logs or transcripts, and revoke or rotate it if exposed. <br>
Risk: The release advertises Sketch, XD, export, and code-generation workflows, but the included package only contains Figma parsing and UI checking scripts. <br>
Mitigation: Treat capabilities beyond the included scripts as guidance unless separately implemented, and manually review generated reports or code before relying on them. <br>


## Reference(s): <br>
- [Figma API endpoint used by included parser](https://api.figma.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/xiaochunz030-spec/software-ui-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON reports and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user-provided design file paths, Figma file keys, brand color rules, and a Figma Personal Access Token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
