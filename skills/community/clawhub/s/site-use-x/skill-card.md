## Description:

Helps agents use the site-use CLI to collect, search, inspect, and cache Twitter/X posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williampenrose](https://clawhub.ai/user/williampenrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up site-use, retrieve Twitter/X timelines, search posts, inspect tweet details and replies, capture screenshots, and query cached local posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the third-party site-use npm package and an authenticated browser session.

Mitigation: Install only when the site-use package is trusted and use an isolated Chrome profile for Twitter/X login.

Risk: Live timeline fetches, searches, tweet lookups, and screenshots may expose account-linked activity to X and store collected posts locally.

Mitigation: Use cache-only commands when live browser access is not needed, and limit returned fields to the minimum needed for the task.

Risk: Twitter/X rate limits or account enforcement can interrupt collection workflows.

Mitigation: Stop live Twitter/X commands during rate-limit cooldowns and rely on local cache queries until it is appropriate to retry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/williampenrose/skills/site-use-x)
- [site-use Homepage](https://github.com/WilliamPenrose/site-use)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses concise field selections for fetched posts and can direct agents to cached local data when live fetching is unnecessary or rate-limited.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
