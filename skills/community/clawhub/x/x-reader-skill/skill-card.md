## Description:

Read X (Twitter) posts without official API. Supports both Nitter (free) and RapidAPI (detailed) methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dkimiscoding](https://clawhub.ai/user/dkimiscoding)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use X Reader to fetch public X/Twitter post content and metadata from a tweet URL or tweet ID, using Nitter by default or RapidAPI when an API key is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet URLs, tweet IDs, or usernames may be sent to RapidAPI or public Nitter instances.

Mitigation: Install only in contexts where sending those request values to the selected external service is acceptable.

Risk: RapidAPI mode uses RAPIDAPI_KEY as an API credential.

Mitigation: Set RAPIDAPI_KEY only in environments where this skill should be allowed to use that credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dkimiscoding/skills/x-reader-skill)
- [RapidAPI Twitter API45](https://rapidapi.com/alexanderxbx/api/twitter-api45)
- [Nitter public instance](https://nitter.net)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tweet content and metadata when available; failures are returned as JSON error objects.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
