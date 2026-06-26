## Description: <br>
车辆工程总体设计CAD图纸生成。当用户说"车辆工程总体设计"、"生成车辆工程总体设计图纸"、"做一个车辆工程总体设计"、"vehicle"时使用此 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Vehicle engineers and CAD workflow users use this skill to collect vehicle design parameters, calculate vehicle engineering outputs, and create guest-access production sheets through the JXT mechanical parts platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle design inputs and generated production-sheet references are sent to jixietools.com. <br>
Mitigation: Use the skill only when that service is approved for the design data being entered. <br>
Risk: Guest production-sheet codes and links can expose production-sheet status or outputs to anyone who has them. <br>
Mitigation: Treat guest codes and links as sensitive and avoid sharing them outside the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liv09370/vehicle) <br>
- [Publisher profile](https://clawhub.ai/user/liv09370) <br>
- [JXT API base URL](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Chinese Markdown with tables and inline bash/curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guided prompts, calculated parameter summaries, production-sheet links, and progress updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
