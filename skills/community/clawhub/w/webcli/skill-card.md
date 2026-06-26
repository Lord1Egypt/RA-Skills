## Description: <br>
Enables agents to browse the web, read page content, click buttons, fill forms, take screenshots, and capture accessibility snapshots through the webcli headless browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erdinccurebal](https://clawhub.ai/user/erdinccurebal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect websites, gather page information, automate browser interactions, fill forms, and capture screenshots or accessibility snapshots during web tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser automation can affect authenticated sessions, cookies, storage, uploads, and page JavaScript. <br>
Mitigation: Use non-sensitive sessions when possible and require explicit approval before uploads, purchases, account changes, cookie or session export, storage changes, or custom JavaScript. <br>
Risk: Saved browser session files and exported cookies may expose private account state. <br>
Mitigation: Delete saved session files after use and avoid exporting cookies unless the user explicitly needs it. <br>
Risk: The skill depends on an external npm package and a Playwright browser installation. <br>
Mitigation: Review the external npm package before installing and deploy only where full browser automation is intended. <br>


## Reference(s): <br>
- [webcli homepage](https://webcli.erdinc.curebal.dev/) <br>
- [webcli repository](https://github.com/erdinccurebal/webcli) <br>
- [ClawHub skill page](https://clawhub.ai/erdinccurebal/webcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser navigation, interaction, screenshot, PDF, storage, cookie, and JavaScript execution commands.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
