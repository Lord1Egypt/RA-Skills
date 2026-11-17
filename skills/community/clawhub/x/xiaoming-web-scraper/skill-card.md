## Description:

Web Scraper Pro helps agents scrape web data, export tables, and schedule recurring collection jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect authorized web data for ecommerce price monitoring, competitor data collection, market research, and general data gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scrape websites or APIs outside the user's authorization or against site policies.

Mitigation: Use it only on sites and APIs the user is authorized to access, and review robots.txt and rate limits before collection.

Risk: Exports and downloaded images may store sensitive or regulated data in unexpected locations.

Mitigation: Verify where CSV, Excel, and image outputs are stored and review exported content before sharing or retaining it.

Risk: Scheduled scraping jobs may continue running after the immediate task is complete.

Mitigation: Confirm how scheduled jobs can be listed, monitored, and removed before enabling recurring collection.

Risk: Installing through an unpinned package command may pull a newer or unexpected installer version.

Mitigation: Prefer a pinned and trusted ClawHub installer version when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/xiaoming-web-scraper)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and exported CSV/Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create scheduled scraping jobs, exported tables, and downloaded images; use only on authorized sites.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
