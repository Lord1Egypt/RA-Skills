## Description: <br>
Automate browser tasks using Selenium, including form filling, web scraping, UI testing, button clicks, alert handling, and screenshot capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panchenbo](https://clawhub.ai/user/panchenbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to create or run Selenium workflows for browser interaction, data extraction, form submission, UI checks, and screenshot capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive form values may be exposed through command-line arguments, logs, or screenshots. <br>
Mitigation: Avoid passing passwords or private form values through command-line arguments, redact logs, and disable default screenshots when handling sensitive data. <br>
Risk: Automated form submission or work-record changes may occur with too little user control. <br>
Mitigation: Review target scripts before use on real accounts and add explicit confirmation before any submit or record-changing action. <br>
Risk: Running arbitrary sites with the browser sandbox disabled can increase exposure to malicious web content. <br>
Mitigation: Use trusted targets, keep browser sandboxing enabled where possible, and avoid running arbitrary sites with sandbox-disabling options. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/panchenbo/selenium-automation-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; scripts may also produce CSV, JSON, and screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser automation may interact with live websites and local browser drivers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
