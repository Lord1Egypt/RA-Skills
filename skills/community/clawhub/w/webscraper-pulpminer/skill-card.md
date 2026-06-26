## Description: <br>
Converts webpages into structured JSON through PulpMiner's AI scraping API, with support for saved APIs, custom schemas, dynamic URLs, and automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melvin2016](https://clawhub.ai/user/melvin2016) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data teams, and automation builders use this skill to configure and call PulpMiner saved APIs that extract structured JSON from webpages for scraping, monitoring, lead generation, price tracking, and data pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target webpage content, extraction parameters, and results are sent to PulpMiner as part of the scraping workflow. <br>
Mitigation: Use the skill only for pages and data you are authorized to process, and avoid submitting confidential or sensitive content unless your organization has approved that use. <br>
Risk: The skill requires a PulpMiner API key and API calls consume credits. <br>
Mitigation: Store the API key securely, avoid exposing it in prompts or logs, and monitor credit usage for saved APIs. <br>
Risk: Zapier callback integrations can forward scraped results to external workflows. <br>
Mitigation: Use callback URLs only for workflows and destinations you trust. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/melvin2016/webscraper-pulpminer) <br>
- [PulpMiner website](https://pulpminer.com) <br>
- [PulpMiner API dashboard](https://pulpminer.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PULPMINER_API_KEY; API responses return JSON with data and errors fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
