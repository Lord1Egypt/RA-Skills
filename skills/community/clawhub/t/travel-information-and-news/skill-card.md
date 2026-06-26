## Description: <br>
Searches and aggregates travel news, destination information, and hotel or attraction reviews from Tavily, optional Brave Search, and optional browser scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NHZallen](https://clawhub.ai/user/NHZallen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planning professionals, travel agents, tour operators, and travel content creators use this skill to collect current destination information, tourism news, visa or policy updates, travel tips, and review summaries for planning and content preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel queries may be sent to Tavily and, when enabled, Brave Search or browser-visited sites. <br>
Mitigation: Avoid confidential client, visa, health, booking, or account details unless those providers are approved for that data. <br>
Risk: Optional browser scraping can interact with third-party sites that may have their own rules and session risks. <br>
Mitigation: Keep browser scraping disabled unless needed, avoid logged-in sessions, review target-site rules, and run the browser stack in a contained environment. <br>


## Reference(s): <br>
- [Travel Information and News on ClawHub](https://clawhub.ai/NHZallen/travel-information-and-news) <br>
- [Tavily](https://tavily.com) <br>
- [Brave Search API](https://brave.com/search/api) <br>
- [Desktop Control skill](https://clawhub.com/skills/desktop-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Plain text, DOCX, or PDF travel report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include detected-language metadata; output language should match the user's query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
