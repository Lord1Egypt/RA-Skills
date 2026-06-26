## Description: <br>
Web Access.Bak guides an agent through web search, page retrieval, authenticated browser operations, and dynamic web interaction using tool selection and optional Chrome CDP control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aysun168](https://clawhub.ai/user/aysun168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when an assistant needs to gather or verify online information, read web pages, or operate logged-in and dynamic sites through an authorized browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent act through a logged-in Chrome session, including sensitive sites or account actions. <br>
Mitigation: Use a separate Chrome profile or low-privilege account, disable remote debugging when finished, stop the proxy when not in use, and require explicit approval before uploads, posts, purchases, deletions, account changes, or sensitive browsing. <br>
Risk: Automated browsing can interact with pages in ways the user did not intend or trigger site anti-abuse controls. <br>
Mitigation: Keep actions goal-scoped, review proposed page operations before execution, prefer primary sources for verification, and close agent-created tabs after the task. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/aysun168/web-access-bak) <br>
- [CDP Proxy API reference](artifact/references/cdp-api.md) <br>
- [Web Access design article](https://mp.weixin.qq.com/s/rps5YVB6TchT9npAaIWKCw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text, Markdown] <br>
**Output Format:** [Markdown instructions with inline shell and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser automation through a local Chrome CDP proxy when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
