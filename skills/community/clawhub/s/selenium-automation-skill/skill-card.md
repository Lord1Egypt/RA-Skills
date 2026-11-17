## Description:

Automate browser tasks using Selenium, including form filling, web scraping, UI testing, button clicks, alert handling, and capturing screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to drive Selenium-based browser workflows for form submission, data extraction, UI checks, navigation, alert handling, and screenshot capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit forms or time entries and may act on unintended pages or accounts.

Mitigation: Run it only against approved sites with non-sensitive test accounts unless the target workflow has been reviewed.

Risk: Form inputs, scraped data, logs, and screenshots may expose credentials or confidential information.

Mitigation: Avoid passing real passwords or confidential data on the command line, inspect generated files before sharing, and run in isolated workspaces.

Risk: Browser drivers and dependencies are installed at runtime and may vary across environments.

Mitigation: Prefer pinned dependencies and preapproved browser drivers.

## Reference(s):

- [Selenium Automation Skill](https://clawhub.ai/panchenbo/skills/selenium-automation-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create scraped output files and screenshots when the bundled automation scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
