## Description: <br>
Control Steel.dev cloud browser sessions for web automation, form filling, screenshots, content extraction, and browser-use agent loops through Playwright selectors and shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EYHN](https://clawhub.ai/user/EYHN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to start and control Steel.dev cloud browser sessions for web automation, scraping, page interaction, screenshots, and browser-use workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted selectors, URLs, filenames, page text, model-generated inputs, or JavaScript can trigger unsafe local Python execution through command wrappers. <br>
Mitigation: Review and fix argument handling before passing untrusted or model-generated values into the scripts. <br>
Risk: Cloud browser operation can expose page content, screenshots, account interactions, and browsing activity to Steel.dev processing. <br>
Mitigation: Avoid sensitive or regulated accounts unless this processing is acceptable for the use case. <br>
Risk: The Steel API key and active sessions grant access to browser automation resources. <br>
Mitigation: Protect STEEL_API_KEY, avoid logging secrets, and release sessions when work is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EYHN/steel-browser) <br>
- [Steel.dev](https://steel.dev) <br>
- [Steel.dev API keys dashboard](https://app.steel.dev) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, files, configuration, guidance] <br>
**Output Format:** [CLI text output, PNG screenshot files, and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STEEL_API_KEY and may persist a Steel session ID in local state until released.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
