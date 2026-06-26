## Description: <br>
Guides agents through web search, page reading, logged-in browser operations, dynamic content handling, and Chrome DevTools Protocol automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deardavidzheng](https://clawhub.ai/user/deardavidzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to select appropriate web access methods, operate browser sessions when needed, and gather or interact with online content through search, direct fetches, and CDP-driven browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real logged-in Chrome profile through a local browser-control service. <br>
Mitigation: Use a dedicated browser profile or test accounts, and stop the proxy when it is not needed. <br>
Risk: Browser automation may submit forms, upload local files, publish content, make purchases, delete data, or change account settings. <br>
Mitigation: Require explicit user approval before uploads, public posts, form submissions, purchases, deletions, account changes, or visits to sensitive private sites. <br>


## Reference(s): <br>
- [ClawHub Web Access Skill](https://clawhub.ai/deardavidzheng/web-access-skill) <br>
- [CDP Proxy API reference](references/cdp-api.md) <br>
- [Web Access article](https://mp.weixin.qq.com/s/rps5YVB6TchT9npAaIWKCw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code snippets, and structured summaries when useful.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-operation instructions, CDP API calls, extracted web content, screenshots, and file-upload actions depending on the user task.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
