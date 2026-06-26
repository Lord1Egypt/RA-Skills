## Description: <br>
Browser automation guidance for agents using Smooth CLI to navigate websites, authenticate, fill forms, extract data, test web apps, and automate browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoniocirclemind](https://clawhub.ai/user/antoniocirclemind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate browser sessions through Smooth CLI for web interaction, scraping, testing, authentication workflows, structured extraction, and multi-step browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Smooth can operate authenticated browser sessions and persistent profiles through an external browser automation service. <br>
Mitigation: Use separate profiles per account, require explicit user confirmation before login or account-changing actions, close sessions when finished, and delete profiles that are no longer needed. <br>
Risk: Uploaded files and downloaded session artifacts may expose sensitive or confidential information. <br>
Mitigation: Avoid uploading secrets or confidential documents unless necessary, limit files to the task, and delete uploaded files or session artifacts when finished. <br>
Risk: Browser automation and JavaScript execution can change page state, submit forms, or act on unintended sites. <br>
Mitigation: Constrain sessions with allowed URL patterns where possible and require explicit confirmation before JavaScript execution, file transfer, or actions that alter accounts or data. <br>


## Reference(s): <br>
- [Smooth app and API key portal](https://app.smooth.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes session, profile, file, extraction, and JavaScript execution command patterns; structured output may follow caller-provided JSON schemas.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
