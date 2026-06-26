## Description: <br>
Automate web form interactions including login, file upload, text input, and form submission using Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingzl](https://clawhub.ai/user/flyingzl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate browser-based form workflows, including authenticated sessions, file uploads, text entry, option selection, submission, and screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent browser-control power over arbitrary websites, including form submission. <br>
Mitigation: Inspect the configuration before execution and confirm the exact website, fields, files, and submit action. <br>
Risk: The skill can load login sessions from cookies, localStorage, or sessionStorage. <br>
Mitigation: Avoid sensitive session files unless necessary and run browser automation in an isolated environment. <br>
Risk: The skill can upload local files and force-click submit controls. <br>
Mitigation: Confirm upload paths and target selectors before running, especially on untrusted or production websites. <br>


## Reference(s): <br>
- [Web Form Automation ClawHub Page](https://clawhub.ai/flyingzl/web-form-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript, shell command, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser automation scripts, form-submission configuration, image-compression commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
