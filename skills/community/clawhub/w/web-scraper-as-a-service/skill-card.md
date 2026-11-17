## Description:

Build client-ready web scrapers with clean data output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanwyngaard](https://clawhub.ai/user/seanwyngaard)

### License/Terms of Use:


## Use Case:

Developers and data practitioners use this skill to turn target URLs or scraping briefs into client-ready scraper projects with cleaned CSV/JSON data, a data quality report, documentation, and handoff notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping websites without authorization or contrary to robots.txt or terms of service can create legal, operational, or platform-policy risk.

Mitigation: Use the skill only for websites the user is authorized to scrape, review robots.txt and terms first, and document any terms that prohibit scraping.

Risk: Generated scraper code may behave unexpectedly or place excessive load on a target website.

Mitigation: Inspect generated Python before running it, keep rate limits and retry settings conservative, and run scrapers inside a dedicated workspace.

Risk: User-agent rotation can obscure scraper identity if used carelessly.

Mitigation: Prefer an honest, project-identifying User-Agent and avoid using rotation to bypass access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanwyngaard/skills/web-scraper-as-a-service)
- [Publisher profile](https://clawhub.ai/user/seanwyngaard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown with generated Python project files and CSV/JSON data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scraper code, requirements, configuration, cleaned data files, quality reports, documentation, and client handoff notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
