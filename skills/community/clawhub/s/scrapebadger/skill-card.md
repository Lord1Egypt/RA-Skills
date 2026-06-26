## Description: <br>
Web scraping platform for Twitter/X data, Vinted marketplace data, and general web scraping API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xghostcasper](https://clawhub.ai/user/0xghostcasper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call ScrapeBadger APIs for Twitter/X lookups, Vinted marketplace queries, page scraping, screenshots, anti-bot detection, structured extraction, and batch scraping jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ScrapeBadger API key and API calls can consume credits. <br>
Mitigation: Use a revocable key, keep it in SCRAPEBADGER_API_KEY, monitor account usage and credits, and rotate the key if exposure is suspected. <br>
Risk: Scraping requests may send target URLs, page content, prompts, or extraction criteria to an external service. <br>
Mitigation: Avoid submitting secrets, internal-only URLs, personal data, or regulated content unless authorized to send that data to ScrapeBadger. <br>
Risk: Using scraping endpoints against third-party sites can create compliance or terms-of-service risk. <br>
Mitigation: Confirm that the requested targets and data collection are authorized before running scraping, screenshot, extraction, or batch jobs. <br>


## Reference(s): <br>
- [ScrapeBadger Documentation](https://docs.scrapebadger.com) <br>
- [ScrapeBadger Dashboard](https://scrapebadger.com/dashboard) <br>
- [ScrapeBadger MCP Server](https://mcp.scrapebadger.com/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/0xghostcasper/scrapebadger) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP endpoint examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCRAPEBADGER_API_KEY and sends requests to ScrapeBadger's external APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
