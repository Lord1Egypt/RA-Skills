## Description: <br>
Uses Playwright MCP, browser-use CLI, and the OpenClaw browser to plan and run web product QA tests, capture bug screenshots, report findings, and optionally file Coding issues after confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyin717](https://clawhub.ai/user/wangyin717) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to explore a target web app, propose a concise functional test plan, execute confirmed tests, document bugs with screenshots, and prepare Coding issue entries after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that this browser-testing skill can weaken browser protections and use high-risk browsing options without enough scoping or warnings. <br>
Mitigation: Use isolated test accounts and browser profiles, avoid production credentials, and require explicit approval before changing SSRF allowlists, disabling sandboxing, using cloud or proxy features, creating tunnels, or reusing local Chrome sessions. <br>
Risk: Automated QA may handle credentials, screenshots, local services, and authenticated sessions. <br>
Mitigation: Limit testing to approved targets, redact sensitive data from reports and screenshots, and review any generated Coding issues before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyin717/skills/testagent-browser-testing) <br>
- [Browser Testing Reference](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown test plans and reports with inline commands, screenshot paths, and issue-filing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MEDIA screenshot references and Coding issue details after user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
