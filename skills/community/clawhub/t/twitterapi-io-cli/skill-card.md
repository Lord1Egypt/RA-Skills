## Description:

Fetch and paginate Twitter/X data using twitterapi.io. Use when you need to fetch one tweet, fetch a user profile, get recent tweets for a user, fetch replies, quote tweets, thread context, or mentions, or run twitterapi.io advanced search queries without hand-rolling raw API requests each time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ropl-btc](https://clawhub.ai/user/ropl-btc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run read-only twitterapi.io CLI workflows for tweets, user profiles, timelines, replies, quotes, thread context, mentions, and advanced search while keeping requests narrow and JSON-parsable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing a third-party CLI from an unpinned GitHub source, so reviewed code could differ from installed code.

Mitigation: Install only a pinned, audited release or commit of the twitterapi-io CLI before use.

Risk: The CLI handles a twitterapi.io API key and may store it in a local config file.

Mitigation: Use a narrowly scoped, revocable API key; avoid passing secrets on the command line; and treat the local config file as sensitive.

Risk: Timeline and search workflows can become broad or high-cost if limits are expanded without review.

Mitigation: Keep reads narrow, use explicit limits and time filters, and stop for review before adding broad scraping defaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ropl-btc/skills/twitterapi-io-cli)
- [Package repository](https://github.com/ropl-btc/twitterapi-io-cli)
- [twitterapi.io docs links](references/links.md)
- [twitterapi.io documentation index](https://docs.twitterapi.io/llms.txt)
- [twitterapi.io authentication](https://docs.twitterapi.io/authentication)
- [twitterapi.io advanced search endpoint](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workflows; compact JSON by default with optional raw endpoint payloads.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
