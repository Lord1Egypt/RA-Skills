## Description: <br>
ToolDeck saves user-confirmed public tool and service URLs by scraping page details, categorizing them, and storing the resulting records in a personal JSON database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almohalhel1408](https://clawhub.ai/user/almohalhel1408) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use ToolDeck to save, retrieve, and suggest tool or service records from explicitly provided public URLs in a personal database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests OAuth, purchase, and crypto capability tags that do not match the described bookmarker workflow. <br>
Mitigation: Before installation, confirm the platform is not granting unnecessary OAuth, purchase, or crypto permissions. <br>
Risk: Public URL scraping can capture sensitive content or identifiers if boundaries are not followed. <br>
Mitigation: Scrape only explicitly provided public URLs, respect robots.txt, skip authenticated or private pages, and strip tracking parameters, OAuth tokens, API keys, and session IDs before saving. <br>
Risk: Saved tool records persist in a local JSON database. <br>
Mitigation: Only save entries after user confirmation and only for public tool pages the user is comfortable keeping locally. <br>


## Reference(s): <br>
- [ToolDeck ClawHub page](https://clawhub.ai/almohalhel1408/tooldeck) <br>
- [database.json](references/database.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Text] <br>
**Output Format:** [Markdown confirmation text plus structured JSON database entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before saving entries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
