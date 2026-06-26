## Description: <br>
Guides agents in choosing between structured platform adapters and browser automation for web scraping and data collection tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbozhao279-code](https://clawhub.ai/user/wenbozhao279-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to select an appropriate scraping approach for social media, ecommerce, monitoring, and structured data extraction workflows. It helps decide when to use opencli adapters for JSON output and when to use playwright-cli for browser-based collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer an agent to use active browser logins for scraping. <br>
Mitigation: Use dedicated or test browser profiles, avoid personal or production accounts, and verify authorization before collecting target data. <br>
Risk: Scraping workflows may collect private or personal data or exceed the intended scope. <br>
Mitigation: Define the approved collection scope, avoid private or personal data unless explicitly permitted, and review target platform rules before running commands. <br>
Risk: Browser state reuse can expose logged-in sessions to unintended automation. <br>
Mitigation: Keep scraping sessions isolated, confirm which profile and tabs are active, and close or reset sessions after the task is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wenbozhao279-code/web-scraping-tool-selection-strategy) <br>
- [Web scraping platform and tool mapping reference](artifact/references/platform-tool-mapping-reference.md) <br>
- [Browser state reuse guide](artifact/references/browser-state-reuse-guide.md) <br>
- [Data extraction patterns reference](artifact/references/data-extraction-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific command examples, browser session prerequisites, and data formatting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
