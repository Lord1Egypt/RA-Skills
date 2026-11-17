## Description:

Scrapes public X.com (Twitter) tweet history using three Playwright-based strategies: auto-search, browser-session GraphQL access, and DOM scrolling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to configure and run Playwright-based X.com collection workflows for public tweet archives. It supports local JSON collection for analysis, backup, or migration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires exporting live X.com login cookies, which can expose an authenticated session if mishandled.

Mitigation: Treat the cookie file like a password: keep it out of source control, restrict local file access, delete it after use, and consider revoking the browser session afterward.

Risk: Authenticated scraping can affect the account used for collection and may not be appropriate for a primary account.

Mitigation: Use a dedicated low-risk account or isolated browser profile for collection.

Risk: The scripts can overwrite or merge into seed JSON files during collection.

Mitigation: Back up seed JSON files before running the scripts or using auto-merge behavior.

Risk: The workflow installs and runs browser automation dependencies locally.

Mitigation: Install dependencies in an isolated environment and pin versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/x-tweet-scraper)
- [Workflow reference](references/workflow.md)
- [X.com](https://x.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python scripts and local JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tweet datasets, ID lists, cursor/checkpoint state, and optional merged seed JSON files under a username-specific data directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
