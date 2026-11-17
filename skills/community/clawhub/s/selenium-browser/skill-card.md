## Description:

Start a Selenium-controlled Chrome browser, open a URL, take a screenshot, and report progress; supports headless mode and optional proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreybespalov89](https://clawhub.ai/user/andreybespalov89)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to launch a Selenium-controlled Chrome or Chromium browser, navigate to a supplied URL, and capture browser output such as screenshots or progress messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can expose users to arbitrary web content with weakened browser isolation.

Mitigation: Restrict or confirm target URLs, remove --no-sandbox unless equivalent container isolation is present, and review the browser launch configuration before deployment.

Risk: The security review says the packaged script and documentation disagree in ways that could leave browsers running.

Mitigation: Make the shipped script match the documented screenshot-and-exit workflow and enforce explicit termination or timeout behavior.

Risk: The security guidance calls out dependency and invocation hardening needs.

Mitigation: Use explicit invocation, pin and verify Selenium and browser-driver dependencies, and review the skill before installation.

## Reference(s):

- [Selenium + Chrome Setup Guide](references/setup.md)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Text status or error messages with setup guidance and a screenshot file path when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on local Chrome, ChromeDriver, Selenium, URL access, and optional proxy configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
