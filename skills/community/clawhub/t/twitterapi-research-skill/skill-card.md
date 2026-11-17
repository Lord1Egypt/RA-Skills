## Description:

General-purpose X/Twitter research agent that searches and summarizes real-time discourse, profiles, tweet threads, and account watchlists through twitterapi.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blascokoa](https://clawhub.ai/user/blascokoa)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to research X/Twitter discussions from an agent session, including topic searches, profile checks, conversation threads, and watchlist monitoring. It helps produce sourced briefings, raw JSON, markdown research notes, and concise terminal summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: X/Twitter research queries and fetched results are sent through twitterapi.io, a third-party API.

Mitigation: Use explicit, scoped search requests and install only when sharing those queries with twitterapi.io is acceptable.

Risk: Using an overbroad shared environment file can expose unrelated secrets to an agent session.

Mitigation: Set only TWITTERAPI_IO_KEY in the environment for this skill and keep unrelated credentials out of shared global environment files.

Risk: Broad searches or unattended watchlist checks can consume API credits and surface noisy results.

Mitigation: Prefer quick mode, narrow operators, limits, and manual review before running broad or recurring checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blascokoa/skills/twitterapi-research-skill)
- [twitterapi.io](https://twitterapi.io)
- [Bun](https://bun.sh)
- [Claude Code](https://code.claude.com)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON, and Markdown research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save Markdown research files and cache repeated query results locally.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
