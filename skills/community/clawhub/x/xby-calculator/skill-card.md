## Description: <br>
A Model Context Protocol calculator skill that routes arithmetic, trigonometry, statistics, combinatorics, number theory, complex-number, matrix, numerical-analysis, finance, unit-conversion, and geometry requests to calculator tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for a broad range of calculator and mathematical operations. The skill selects the appropriate calculator function, gathers required parameters, calls the Xiaobenyang API, and returns the result to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calculator inputs are sent to a third-party Xiaobenyang API. <br>
Mitigation: Avoid sensitive business, financial, research, or personal calculations unless the API service, data handling, and retention practices are acceptable for the use case. <br>
Risk: The skill stores the XBY_APIKEY value in a plaintext .env file in the working directory. <br>
Mitigation: Protect the workspace, do not commit the .env file, use a scoped key where available, and rotate the key if the workspace or file contents may have been exposed. <br>
Risk: The security evidence recommends review before installation. <br>
Mitigation: Review the skill behavior and configuration before use, and install it only when the third-party API dependency and local key storage are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-calculator) <br>
- [Xiaobenyang API service](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, API Calls, guidance, configuration] <br>
**Output Format:** [Text or structured API response summarized for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value before calculator API calls can run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
