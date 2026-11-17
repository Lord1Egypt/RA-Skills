## Description:

Teaches the agent how to perform advanced web automation using Python, Selenium WebDriver, and ChromeDriver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gg-erick](https://clawhub.ai/user/gg-erick)

### License/Terms of Use:


## Use Case:

Developers and automation-focused agents use this skill to draft Selenium WebDriver scripts for browser navigation, screenshots, JavaScript execution, and element interaction. It is intended for browser automation tasks where the user reviews generated code and approves execution separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Chrome setup disables the browser sandbox, reducing browser isolation.

Mitigation: Use an isolated, non-privileged environment, pin Selenium dependencies, and remove --no-sandbox unless it is explicitly needed for a disposable container.

Risk: Generated browser automation can navigate websites, write files, and execute user-provided interaction flows.

Mitigation: Review generated scripts before use and require explicit user approval before running automation code.

## Reference(s):

- [Selenium Automation on ClawHub](https://clawhub.ai/gg-erick/skills/selenium-browser-skill)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated automation scripts require user review and explicit approval before execution.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
