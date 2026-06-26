## Description: <br>
悬架CAD图纸生成。当用户说"悬架"、"生成悬架图纸"、"做一个悬架"、"suspension"时使用此 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Engineers and mechanical design users use this skill to generate suspension CAD drawing workflows by selecting a suspension product, entering design parameters, reviewing calculated results, and creating a guest production sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suspension design parameters are sent to jixietools.com, and the workflow can create a guest production sheet there. <br>
Mitigation: Avoid proprietary or customer-sensitive engineering data unless the user trusts that service, and confirm before calculation or production-sheet creation. <br>
Risk: Engineering calculations and production-sheet outputs may be unsuitable if inputs are wrong or the external service response is unexpected. <br>
Mitigation: Have a qualified reviewer check the entered parameters, calculated results, and generated production sheet before using them for manufacturing or design decisions. <br>


## Reference(s): <br>
- [Suspension ClawHub release](https://clawhub.ai/liv09370/suspension) <br>
- [Publisher profile](https://clawhub.ai/user/liv09370) <br>
- [JixieTools API base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Chinese Markdown with tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the user one parameter at a time and uses returned filenames and guest codes to continue the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
