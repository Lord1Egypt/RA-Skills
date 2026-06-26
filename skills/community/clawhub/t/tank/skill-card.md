## Description: <br>
储罐CAD图纸生成。当用户说"储罐"、"生成储罐图纸"、"做一个储罐"、"tank"时使用此 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide Chinese-language tank CAD drawing workflows for horizontal or vertical storage tanks. It collects tank design parameters, calls the JXT/Jixietools API for calculation and production sheet creation, and helps monitor guest-accessible production status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends user-provided tank design parameters to jixietools.com. <br>
Mitigation: Confirm that users are comfortable sharing the design inputs with JXT/Jixietools before running API calls. <br>
Risk: Guest codes and viewing links may allow anyone with the link to view production sheet details or status. <br>
Mitigation: Treat guest codes and viewing links like passwords and avoid posting them in public or shared channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liv09370/tank) <br>
- [Jixietools API Base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Chinese Markdown guidance with inline curl commands and tabular parameter summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains the returned filename across incremental calculations and treats generated guest links as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
