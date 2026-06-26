## Description: <br>
Captures screenshots of local or remote web pages with Puppeteer in headless Chromium, including login-required SPAs, and writes PNG images plus optional result metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to automate screenshots of public or authenticated web application pages for UI review, documentation, and release evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Login credentials can be exposed if reusable config files are shared or committed. <br>
Mitigation: Use test or least-privileged accounts and keep configs containing credentials out of version control. <br>
Risk: Screenshots and result.json can contain sensitive application data. <br>
Mitigation: Write outputs to an approved private directory and review them before sharing. <br>
Risk: storeLogin invokes an application store method directly. <br>
Mitigation: Use storeLogin only for applications you control and when the exact store method and arguments are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aowind/sjht-web-screenshot) <br>
- [Publisher profile](https://clawhub.ai/user/aowind) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [PNG screenshots and result.json metadata generated from a JSON configuration file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided target URLs, page names, output directory, viewport size, and optional login selectors or store-login settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
