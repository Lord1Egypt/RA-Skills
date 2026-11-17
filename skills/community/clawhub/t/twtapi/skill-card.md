## Description:

Access live Twitter/X data through TwtAPI's hosted public skill gateway. Search tweets, look up users, read timelines, inspect followers and following, fetch tweet details, and check trends with structured JSON for OpenClaw and other compatible skill runners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonygjj](https://clawhub.ai/user/tonygjj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query live Twitter/X data through TwtAPI, including searches, user profiles, timelines, followers, following, tweet details, and trends. It is suited for workflows that need structured social-media data returned to compatible skill runners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X search terms, account or tweet identifiers, and returned content are sent through TwtAPI's hosted service.

Mitigation: Install and use the skill only when that third-party data handling is acceptable for the intended workflow.

Risk: A custom TWTAPI_SKILL_BASE_URL can route requests and the dedicated skill key to an untrusted endpoint.

Mitigation: Keep TWTAPI_SKILL_BASE_URL unset for normal use, or set it only to a trusted HTTPS endpoint.

Risk: The dedicated TwtAPI skill key may be exposed if used with an HTTP or untrusted custom gateway.

Mitigation: Rotate the skill key if it was ever used with an HTTP endpoint or an endpoint you no longer trust.

## Reference(s):

- [TwtAPI homepage](https://www.twtapi.com/en/)
- [ClawHub skill page](https://clawhub.ai/tonygjj/skills/twtapi)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [Pretty-printed JSON from CLI/API responses, with Markdown setup and usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TWTAPI_SKILL_KEY; most list commands support cursor-based pagination]

## Skill Version(s):

1.2.0 (source: frontmatter, ClawHub metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
