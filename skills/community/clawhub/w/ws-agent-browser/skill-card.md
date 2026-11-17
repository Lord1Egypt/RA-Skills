## Description:

Browser control for automated page actions, screenshots, form filling, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhbillwer](https://clawhub.ai/user/fhbillwer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to direct an agent through browser tasks such as opening pages, taking screenshots, filling forms, exporting table data, and monitoring pages for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser control can perform sensitive actions such as logins, form submissions, purchases, account changes, script execution, scraping authenticated pages, or scheduled monitoring.

Mitigation: Require explicit confirmation before sensitive actions and review requested browser operations before execution.

Risk: Screenshots, scraped data, and configuration files may contain sensitive information.

Mitigation: Check storage locations for generated browser data and delete screenshots, exports, recordings, and configuration files when no longer needed.

Risk: Automated scraping or monitoring may conflict with site rules or user expectations.

Mitigation: Respect robots.txt, site terms, and access boundaries before running extraction or monitoring tasks.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with browser action requests, tool names, paths, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, recordings, scraped data exports, and browser configuration files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
