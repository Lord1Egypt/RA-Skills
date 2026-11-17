## Description: <br>
Stagehand Browser Tool Free helps an agent use natural-language browser commands to navigate local Chrome, interact with page elements, capture screenshots, and extract webpage data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, freelancers, and other external users can use this skill to automate local browser tasks such as navigation, page interaction, form filling, screenshots, and structured data extraction. Users should supervise actions that affect accounts, submissions, purchases, or sensitive pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a local Chrome session and perform real website actions. <br>
Mitigation: Use it on non-sensitive pages first and require human confirmation for login, purchase, posting, or form submission actions. <br>
Risk: Page extraction or callback_url use could disclose sensitive page content outside the intended local workflow. <br>
Mitigation: Avoid callback_url and sensitive page extraction unless the user understands where the data will go. <br>
Risk: Privacy and external-callback behavior are under-explained in the release evidence. <br>
Mitigation: Review the skill before deployment and limit use to data and sessions appropriate for browser automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/stagehand-browser-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return browser action status, extracted page data, screenshots, logs, and error details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
