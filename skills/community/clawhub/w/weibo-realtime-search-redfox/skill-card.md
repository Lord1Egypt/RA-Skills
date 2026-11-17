## Description:

Searches Weibo posts by keyword through RedFox, with support for comprehensive, trending, and real-time sorting plus creator verification filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content operators, creators, brand teams, and PR teams use this skill to find fresh Weibo posts, compare engagement signals, paginate results, and optionally subscribe to daily keyword updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and request metadata are sent to RedFox using the configured REDFOX_API_KEY.

Mitigation: Use the skill only when that data sharing is acceptable, and confirm the API key source, scope, expiration, and reset or revocation path before use.

Risk: The daily subscription feature can create persistent scheduled tasks, and the cron fallback may be unsafe with raw keyword input.

Mitigation: Confirm the exact scheduled task before creation, avoid the raw cron fallback, and keep a clear way to list, disable, and delete daily push tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/weibo-realtime-search-redfox)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)
- [Weibo profile URL pattern](https://weibo.com/u/{uid})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and prompts for users, with JSON returned by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include post text links, author information, engagement counts, pagination state, and filter labels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
