## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wechatgpt798](https://clawhub.ai/user/wechatgpt798) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to drive browser workflows through the agent-browser CLI, including navigation, ref-based interaction, page state checks, session isolation, screenshots, PDFs, storage, cookies, and network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser sessions, cookies, local storage, and captured network data can contain sensitive information. <br>
Mitigation: Treat saved auth JSON files and captured browser data as secrets; do not commit them, share them, or print them into logs. <br>
Risk: Browser automation can perform actions against real accounts or live services. <br>
Mitigation: Use least-privilege or test accounts where possible, and confirm that traffic mocking or network interception is authorized before use. <br>
Risk: The skill depends on an external npm command named agent-browser. <br>
Mitigation: Verify that the installed npm package is the intended agent-browser package before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wechatgpt798/wayne-agent-browser) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that interact with browser state, saved sessions, cookies, storage, screenshots, PDFs, and captured network data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
