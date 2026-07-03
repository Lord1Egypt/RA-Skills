## Description: <br>
A sequential-thinking MCP service that breaks complex problems into manageable steps and supports iterative refinement and alternate reasoning paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to structure multi-step reasoning, planning, and problem-solving tasks. The skill routes thought-step inputs to the XiaoBenYang sequential-thinking service and returns the service response for presentation to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sequential-thinking content is sent to the external mcp.xiaobenyang.com service. <br>
Mitigation: Do not use the skill for private, regulated, or sensitive reasoning unless the publisher clarifies data handling. <br>
Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file. <br>
Mitigation: Use a dedicated credential, restrict local file access, and rotate the key if the workspace may have been exposed. <br>
Risk: The security scan verdict is suspicious because the skill presents as a reasoning helper while sending thought data to a third-party API. <br>
Mitigation: Review the publisher, API behavior, and security guidance before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cainingnk/skills/sequentialthinking) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [XiaoBenYang API key page](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Structured tool-call result data summarized as text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY API key and sends thought-step inputs to an external service.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
