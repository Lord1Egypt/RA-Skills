## Description:

A skill for discovering and scraping YouTube channels by category and location without requiring API keys or login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arulmozhiv](https://clawhub.ai/user/arulmozhiv)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to discover YouTube channels, scrape public channel metadata, build queue files, and export structured results for influencer or social media analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy credentials may be exposed through committed configuration, shared logs, or copied command examples.

Mitigation: Treat proxy credentials as secrets, keep them in environment variables or a secret manager, and avoid pasting them into shared logs.

Risk: YouTube scraping with anti-detection and residential proxy techniques may violate platform terms or applicable law.

Mitigation: Confirm the intended scraping activity complies with YouTube's terms and relevant laws before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arulmozhiv/skills/youtube-scrapper)
- [ScrapeClaw](https://www.scrapeclaw.cc/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes generated queue JSON, scraped channel JSON, thumbnail files, and progress files.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
