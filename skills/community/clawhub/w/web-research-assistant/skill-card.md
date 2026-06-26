## Description: <br>
AI-powered web research assistant that leverages BrowserAct API to supplement restricted web access by searching the internet for additional information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to run supplemental web searches through BrowserAct when direct web access is blocked or insufficient. It returns source-backed research summaries for current information gathering, comparison, and data collection tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review states that the documentation promotes bypassing paywalls, CAPTCHA or human checks, and regional restrictions without clear authorization limits. <br>
Mitigation: Use the skill only for lawful, authorized research and do not use it to bypass paywalls, CAPTCHA, anti-bot protections, or regional licensing restrictions. <br>
Risk: Research queries and retrieved content are sent to BrowserAct through an external API. <br>
Mitigation: Do not submit secrets, personal data, or confidential business topics unless BrowserAct's data-handling terms are acceptable for the use case. <br>


## Reference(s): <br>
- [BrowserAct Console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct MCP endpoint](https://mcp.browseract.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON research report with titles, URLs, snippets, extracted statistics, and source citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the report to a user-specified output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
