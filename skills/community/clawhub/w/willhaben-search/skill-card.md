## Description: <br>
Willhaben marketplace search API for finding listings, browsing categories, and getting listing details on Austria's largest classifieds platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Saimo](https://clawhub.ai/user/Saimo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search willhaben.at listings, identify relevant categories, retrieve listing details, and present source listing links for user follow-up. <br>

### Deployment Geography for Use: <br>
Global; results focus on Austria's willhaben marketplace. <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace search terms are sent to the third-party API at api.nochda.at. <br>
Mitigation: Avoid sending sensitive personal information in search queries. <br>
Risk: Search, suggestion, and listing details depend on the availability and freshness of an external marketplace API. <br>
Mitigation: Treat returned listings as discovery results and use the original listing URL for final review. <br>
Risk: Rate limits can interrupt high-volume use. <br>
Mitigation: Respect the documented 50 requests per minute global limit and 10 requests per minute limit for search and suggestion endpoints. <br>


## Reference(s): <br>
- [Willhaben Search API homepage](https://api.nochda.at) <br>
- [ClawHub skill page](https://clawhub.ai/Saimo/willhaben-search) <br>
- [Publisher profile](https://clawhub.ai/user/Saimo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTP examples and JSON response schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses unauthenticated read-only API endpoints; search and suggestion endpoints are rate limited.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
