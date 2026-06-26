## Description: <br>
Hosted browser automation API for agents that supports screenshots, Playwright scripts, workflows, and remote browser execution without local Chrome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davisdiehl](https://clawhub.ai/user/davisdiehl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use Riddle to add hosted browser automation, screenshots, Playwright workflows, form interactions, and network capture to agents without running a local Chromium instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots, network captures, and authenticated browser sessions can send sensitive site data to Riddle's hosted service. <br>
Mitigation: Use test credentials where possible, avoid high-privilege sessions unless necessary, and be careful when enabling HAR capture on private sites. <br>
Risk: Browser automation can submit forms, change account data, or perform purchases when used in authenticated sessions. <br>
Mitigation: Require explicit confirmation before actions that submit forms, change account data, purchase items, or otherwise perform authenticated side effects. <br>
Risk: The skill relies on an external plugin package and hosted service. <br>
Mitigation: Install only if you trust Riddle and the referenced plugin package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davisdiehl/riddle) <br>
- [Riddle website](https://riddledc.com) <br>
- [Riddle docs](https://riddledc.com/docs) <br>
- [Plugin source cited by artifact](https://github.com/riddledc/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with inline shell commands and tool usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The described plugin returns screenshot file paths and can optionally capture HAR network traffic.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
