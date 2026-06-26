## Description: <br>
Guides agents in choosing between web_search, web_fetch, OpenCLI, and browser automation for web research, fetching, fallback handling, login-sensitive workflows, and web-search API configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fmls](https://clawhub.ai/user/fmls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through web search, static page retrieval, structured OpenCLI access, and browser automation fallback decisions. It is especially relevant when searches fail, pages require JavaScript or login state, or API-key configuration guidance is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup path installs global CLI tooling, downloads a browser extension, and may restart Chrome. <br>
Mitigation: Review the setup script before running it, install only from a trusted publisher, and prefer a dedicated browser profile when enabling browser bridge functionality. <br>
Risk: The skill includes workflows for accepting and storing web-search API keys. <br>
Mitigation: Avoid sharing raw API keys in chat unless the workflow protects secrets, confirm provider detection before configuration, and verify stored keys through the intended OpenClaw configuration commands. <br>
Risk: Browser and OpenCLI workflows can involve login state or account-changing actions. <br>
Mitigation: Require user authorization before login, require a second confirmation before irreversible or write actions, and use read-only retrieval when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fmls/web-tools-guide) <br>
- [OpenCLI usage guide](references/opencli-guide.md) <br>
- [Web search API configuration](references/web-search-config.md) <br>
- [Well-known sites index](references/well-known-sites.json) <br>
- [OpenCLI setup script](scripts/setup-opencli.sh) <br>
- [OpenCLI GitHub releases](https://github.com/jackwener/opencli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to read bundled reference files before continuing a web-search, OpenCLI, or browser workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
