## Description: <br>
主轴箱CAD图纸生成。当用户说"主轴箱"、"生成主轴箱图纸"、"做一个主轴箱"、"spindle-box"时使用此 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realsanyu](https://clawhub.ai/user/realsanyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and mechanical design practitioners use this skill to collect spindle-box parameters, request CAD drawing generation through jixietools.com, review calculated values, and monitor guest production-sheet progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends spindle-box design parameters to jixietools.com. <br>
Mitigation: Use the skill only when sharing those design parameters with jixietools.com is acceptable, especially for proprietary CAD work. <br>
Risk: Generated guest URLs and guest_code values act as private access links for production-sheet status and outputs. <br>
Mitigation: Treat guest URLs and guest_code values as confidential and avoid posting them in public chats, tickets, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realsanyu/spindle-box) <br>
- [jixietools API base](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Chinese conversational guidance with Markdown tables, JSON examples, URLs, and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides step-by-step collection of CAD parameters, preserves filename and guest_code values, and polls production-sheet status at five-second intervals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
