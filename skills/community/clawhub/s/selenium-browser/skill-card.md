## Description: <br>
Launches a Selenium-controlled Chrome or Chromium browser for a supplied URL, with optional headless and proxy settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreybespalov89](https://clawhub.ai/user/andreybespalov89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to launch a Selenium-controlled browser session for browser automation, page inspection, or screenshot-oriented workflows from an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised screenshot-and-finish workflow may not match the reviewed script behavior. <br>
Mitigation: Before use, confirm whether the release should produce a screenshot and JSON result or behave as an interactive browser launcher; add a timeout and explicit result handling if screenshot capture is expected. <br>
Risk: The skill opens a supplied URL in a live Selenium-controlled browser session. <br>
Mitigation: Run it only in an isolated browser environment, confirm target URLs before launch, and restrict proxy or network settings to trusted use cases. <br>


## Reference(s): <br>
- [Selenium + Chrome Setup Guide](artifact/references/setup.md) <br>
- [Selenium documentation](https://www.selenium.dev/documentation/) <br>
- [ChromeDriver download page](https://chromedriver.chromium.org/downloads) <br>
- [ClawHub release page](https://clawhub.ai/andreybespalov89/selenium-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and launcher process output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The reviewed security evidence says the artifact advertises screenshot output, but the checked script keeps the browser running without producing the promised screenshot result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
