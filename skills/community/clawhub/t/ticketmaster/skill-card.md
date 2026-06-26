## Description: <br>
Search Ticketmaster events, venues, and attractions with Discovery API filters, market-aware queries, and copy-ready curl and shell helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, event researchers, and agents use this skill to search Ticketmaster listings, venues, attractions, classifications, onsale windows, and API-ready filters through the open Discovery API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, filters, locale, timestamps, event or venue IDs, and the Ticketmaster API key are sent to Ticketmaster. <br>
Mitigation: Install only when sharing this data with Ticketmaster is acceptable; keep TM_API_KEY in the environment and out of local memory, files, screenshots, and pasted examples. <br>
Risk: Discovery API results expose listings and metadata but do not confirm purchases, holds, refunds, or account actions. <br>
Mitigation: Treat the skill as a search and lookup tool; explain the open API boundary before responding to purchase automation requests. <br>
Risk: Broad or deeply paged searches can waste quota and miss supported result boundaries. <br>
Mitigation: Constrain searches with keyword, city, countryCode, marketId, venueId, attractionId, date windows, or classification before paging. <br>


## Reference(s): <br>
- [TicketMaster ClawHub Release](https://clawhub.ai/ivangdavila/ticketmaster) <br>
- [Ticketmaster Discovery API Base Endpoint](https://app.ticketmaster.com/discovery/v2) <br>
- [Ticketmaster Discovery Event Search Endpoint](https://app.ticketmaster.com/discovery/v2/events.json) <br>
- [Ticketmaster Discovery Venue Search Endpoint](https://app.ticketmaster.com/discovery/v2/venues.json) <br>
- [Ticketmaster Discovery Attraction Search Endpoint](https://app.ticketmaster.com/discovery/v2/attractions.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown guidance with inline bash and curl examples; helper commands return JSON from Ticketmaster.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TM_API_KEY and curl; optional jq improves local JSON formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
