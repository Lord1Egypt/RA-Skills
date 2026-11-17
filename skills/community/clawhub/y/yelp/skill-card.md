## Description:

Search Yelp businesses and reviews, compare local options, and audit listing quality with official APIs, public pages, and safe action boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search, compare, and shortlist Yelp businesses, interpret review signals, and prepare owner-authorized listing audits. It is intended for evidence-labeled Yelp workflows using official API data, public Yelp pages, or both.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yelp may receive search terms, location hints, phone numbers, and filter parameters used during live lookups.

Mitigation: Confirm comfort with live Yelp calls before sending sensitive local-search context, and use public-page mode or narrower inputs when appropriate.

Risk: Local notes under ~/yelp/ may retain shortlist decisions, recurring filters, aliases, and audit notes.

Mitigation: Keep storage minimal and redacted, never store API keys or signed request URLs, and confirm before creating local files.

Risk: Owner-side listing work could be mistaken for verified account access or live edit capability.

Mitigation: Stay read-only by default, draft owner-side responses or changes only for authorized users, and do not claim changes are live until the user confirms them.

Risk: Yelp fields such as hours, price, transactions, and delivery status may be stale or unsupported in some markets.

Mitigation: Disclose API, page, or hybrid evidence source, mark weak or stale evidence clearly, and recommend re-checking operational claims before booking, visiting, calling, or ordering.

## Reference(s):

- [ClawHub Yelp Skill](https://clawhub.ai/ivangdavila/skills/yelp)
- [Yelp Skill Homepage](https://clawic.com/skills/yelp)
- [Yelp Business Search API](https://api.yelp.com/v3/businesses/search)
- [Yelp Phone Search API](https://api.yelp.com/v3/businesses/search/phone)
- [Yelp Business Details and Reviews API](https://api.yelp.com/v3/businesses/{id_or_alias})
- [Yelp Delivery Search API](https://api.yelp.com/v3/transactions/delivery/search)
- [Yelp Public Pages](https://www.yelp.com/*)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, concise prose, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs disclose whether evidence came from API, public pages, or a hybrid workflow and include uncertainty or freshness warnings when relevant.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
