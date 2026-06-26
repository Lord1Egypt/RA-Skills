## Description: <br>
Browser automation through the published `@pzeda/super-browser` package and its `super-browser` CLI against a real local Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zipper-319](https://clawhub.ai/user/zipper-319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate a real local Chrome session for rendered-page inspection, navigation, clicks, uploads, screenshots, network review, and browser-based decision workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real logged-in Chrome session, which may affect accounts or sensitive browser state. <br>
Mitigation: Use a separate Chrome profile or test account, and confirm uploads, form submissions, purchases, posts, or other account-changing actions before execution. <br>
Risk: The skill depends on the published npm package `@pzeda/super-browser` and its local CLI behavior. <br>
Mitigation: Install only when the package publisher and installed version are trusted for the environment. <br>
Risk: Browser network inspection may expose sensitive site activity. <br>
Mitigation: Avoid sensitive sites during network inspection and stop the daemon or CDP-enabled browser when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zipper-319/pzeda-super-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, Chrome or Chromium, and a local Chrome CDP session on port 9222.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
