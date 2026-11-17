## Description:

TCGplayer API as structured JSON - search tcgplayer.com cards and sealed products across Pokemon, Magic, Yu-Gi-Oh!, One Piece, Lorcana and every other game (71 product lines), read one product with the market price of every SKU (condition x printing x language) and its recent sale range, page every live seller listing with price, shipping and seller rating, pull up to a year of price history with quantity sold per day or week, the 5 most recent sales, a whole set's price guide, every set of a game, autocomplete, trending searches, and a seller's profile, buyer feedback and catalogue. 13 endpoints, 1 credit each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and card collectors can use the skill to retrieve TCGplayer card and sealed product prices, price history, recent sales, live listings, set guides, and seller information for price checks, collection tracking, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the documented search or product parameters to Scavio and include the API key for authentication.

Mitigation: Review the request data before use and keep SCAVIO_API_KEY in an environment variable or secret store; do not put the key in source code or share it in prompts.

Risk: Security scan confidence is medium and coverage is partial because some path-like references could not be resolved.

Mitigation: Review the referenced paths and skill behavior before installation if you need assurance beyond the available scan.

## Reference(s):

- [TCGplayer Product API Documentation](https://scavio.dev/docs/tcgplayer-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api)
- [Scavio TCGplayer API Overview](https://scavio.dev/tcgplayer-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=tcgplayer-api)

## Skill Output:

**Output Type(s):** [JSON, API data, Guidance]

**Output Format:** [Structured JSON data with Markdown usage guidance and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price, sales, and listing data are returned for the US marketplace in USD; results depend on the requested card SKU and API response.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
