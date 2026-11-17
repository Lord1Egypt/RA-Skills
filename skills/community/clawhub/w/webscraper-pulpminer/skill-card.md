## Description:

Convert any webpage into structured JSON data using AI. Scrape websites, extract data into custom JSON schemas, and call saved APIs programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvin2016](https://clawhub.ai/user/melvin2016)

### License/Terms of Use:


## Use Case:

Developers, data teams, and automation builders use this skill to configure PulpMiner saved APIs, call them with an API key, and retrieve structured JSON from webpages for scraping, extraction, monitoring, lead generation, price tracking, and data pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webpage URLs, scraped content, and extracted results may be processed by PulpMiner as a third-party scraping and LLM-processing service.

Mitigation: Do not submit private or internal URLs, authenticated pages, secrets, regulated data, or sensitive personal information unless approved for that service.

Risk: Zapier callback integrations can send scraped data to an external destination.

Mitigation: Use only approved callback URLs and confirm the destination is authorized to receive the extracted data.

Risk: The PULPMINER_API_KEY grants access to the configured PulpMiner API usage.

Mitigation: Store the API key in an environment variable or approved secret store, avoid logging it, and rotate it if exposure is suspected.

## Reference(s):

- [PulpMiner Website](https://pulpminer.com)
- [PulpMiner API Dashboard](https://pulpminer.com/api)
- [ClawHub Skill Page](https://clawhub.ai/melvin2016/skills/webscraper-pulpminer)
- [ClawHub Publisher Profile](https://clawhub.ai/user/melvin2016)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PULPMINER_API_KEY; saved API responses return JSON with data and errors fields.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
