## Description:

Resolve any place or business name to Tripadvisor ids, then pull ranked restaurants, hotels and attractions in a geo, one location in full, and paged review bodies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve Tripadvisor place names to IDs, retrieve ranked hotels, restaurants, and attractions, inspect a venue, and page through structured review data for travel research, local-business analysis, and reputation monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Venue queries, Tripadvisor URLs or IDs, and SCAVIO_API_KEY are sent to Scavio when the skill is used.

Mitigation: Handle the API key as a secret, avoid submitting sensitive venue queries, and prefer direct HTTPS examples when avoiding SDK installation is important.

Risk: Optional SDK installation can introduce supply-chain exposure in local environments.

Mitigation: Install SDK packages only in isolated environments or use the documented direct HTTPS requests instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/tripadvisor-reviews-api)
- [Scavio Tripadvisor locations documentation](https://scavio.dev/docs/tripadvisor-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=tripadvisor-reviews-api)
- [Scavio rate limits documentation](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tripadvisor-reviews-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response descriptions and Python, JavaScript, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; Tripadvisor API calls return structured JSON envelopes with data and credit usage fields.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
