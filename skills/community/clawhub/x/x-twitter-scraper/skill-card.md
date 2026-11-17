## Description:

Discovers and scrapes public Twitter/X profiles and recent tweets using browser automation, optional search-based profile discovery, and optional proxy configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arulmozhiv](https://clawhub.ai/user/arulmozhiv)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to discover public Twitter/X accounts by location or category, scrape profile and recent tweet data, and export structured datasets for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping public Twitter/X data may conflict with platform terms or applicable privacy requirements.

Mitigation: Confirm the intended use complies with Twitter/X terms and applicable privacy rules before installing or running the skill.

Risk: Profile data, tweet media, queue files, and exports can be retained locally after scraping.

Mitigation: Disable thumbnail downloads when media retention is unnecessary and delete data/output, data/queue, thumbnails, and export files when they are no longer needed.

Risk: Google API keys and proxy credentials may be exposed if stored or shared carelessly.

Mitigation: Treat API keys and proxy credentials as sensitive secrets and avoid committing or publishing configured credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arulmozhiv/skills/x-twitter-scraper)
- [ScrapeClaw suite](https://www.scrapeclaw.cc/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)

## Skill Output:

**Output Type(s):** [JSON, CSV, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples, plus JSON and CSV scraper outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local queue files, profile data files, export files, and downloaded media thumbnails.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
