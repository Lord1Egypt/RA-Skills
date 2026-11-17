## Description:

Scraper for SpielerPlus/TeamPlus team management platform. Extracts events, members, absences, finances, participation stats, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firstsanny](https://clawhub.ai/user/firstsanny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team administrators use this skill to guide authenticated extraction of SpielerPlus/TeamPlus team data such as events, members, absences, finances, participation statistics, profiles, and roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper uses account credentials and can access private team data.

Mitigation: Run it only for accounts and teams you are authorized to access, and store SPIELERPLUS_EMAIL and SPIELERPLUS_PASSWORD outside committed files.

Risk: Scraped results may include sensitive absence, member, participation, or financial information.

Mitigation: Limit sharing of generated output and avoid writing full reports to shared logs or public workspaces.

Risk: Dependency or browser automation behavior may change over time.

Mitigation: Use a reviewed lockfile or pinned dependency versions before running the scraper in shared or production environments.

Risk: Automated scraping may conflict with platform rules or expectations.

Mitigation: Review and follow SpielerPlus/TeamPlus terms and account policies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/firstsanny/skills/spielerplus-scraper)
- [SpielerPlus/TeamPlus](https://www.spielerplus.de)
- [README](README.md)
- [Docker usage example](examples/example-docker.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, JavaScript examples, environment-variable configuration, and optional JSON scraper output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPIELERPLUS_EMAIL and SPIELERPLUS_PASSWORD; generated outputs may contain sensitive team, absence, and financial data.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
