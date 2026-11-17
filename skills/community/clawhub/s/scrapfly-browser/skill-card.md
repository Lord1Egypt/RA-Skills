## Description:

Automate cloud browsers using the Scrapfly Cloud Browser API with Python Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to connect Python Playwright scripts to Scrapfly Cloud Browser for remote browser automation, JavaScript-heavy scraping, geo-targeted browsing, screenshots, downloads, and persistent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional BYOP connector can route browser traffic through a customer's internal network after running a remote installer.

Mitigation: Use BYOP only with network-owner approval, a trusted installer source, host isolation, and a verified install and uninstall process.

Risk: API keys and persistent authenticated sessions can expose credentials or keep access alive beyond the intended workflow.

Mitigation: Store credentials in environment variables or a secrets manager, scope access to the task, and avoid reusing authenticated sessions beyond the intended workflow.

Risk: Forgetting to close Cloud Browser connections can keep remote sessions running and cause continued billing.

Mitigation: Close browser connections in a try/finally block and set session lifetime parameters deliberately.

## Reference(s):

- [Scrapfly Browser Skill Page](https://clawhub.ai/scrapfly/skills/scrapfly-browser)
- [Scrapfly BYOP Exit Peers Documentation](https://scrapfly.io/docs/rpa/exit-peers)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Playwright connection patterns, Scrapfly Cloud Browser URL parameters, session handling notes, and BYOP setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
