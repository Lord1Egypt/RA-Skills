## Description:

Search Ticketmaster events, venues, and attractions with Discovery API filters, market-aware queries, and copy-ready curl and shell helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search Ticketmaster Discovery API listings, venues, attractions, sales windows, and classifications while shaping filters and reusable local defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticketmaster receives search terms, filters, timestamps, IDs, locale, and the API key as query parameters.

Mitigation: Use a dedicated TM_API_KEY, keep it in the environment, and avoid pasting keys into files, screenshots, logs, or shared examples.

Risk: Local memory and saved queries may accumulate preferences, event IDs, venue IDs, or market details.

Mitigation: Periodically review ~/ticketmaster/memory.md and ~/ticketmaster/queries.md and remove preferences or IDs that should no longer be retained.

Risk: Discovery API results can be mistaken for purchase, hold, refund, or seat-locking capability.

Mitigation: Treat the skill as search and lookup guidance only, and explicitly confirm that transaction workflows are outside the open Discovery API surface.

Risk: Broad queries, deep paging, or high request rates may produce noisy results or hit documented Ticketmaster limits.

Mitigation: Constrain queries with city, country, venue, attraction, classification, and date filters before paging, and respect the documented rate and quota limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/ticketmaster)
- [Ticketmaster Discovery API](https://app.ticketmaster.com/discovery/v2)
- [Ticketmaster Discovery Endpoints](artifact/endpoints.md)
- [Query Patterns](artifact/query-patterns.md)
- [Filters and Pagination](artifact/filters-and-pagination.md)
- [Error Handling and Limits](artifact/errors.md)
- [Setup](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide GET requests to Ticketmaster Discovery API and local preference files under ~/ticketmaster/.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
