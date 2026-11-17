## Description:

Aggregates enabled quotedance-service RSS subscriptions through RSSHub and returns a recent, filterable Markdown news digest with local caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoocky](https://clawhub.ai/user/yoocky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users with quotedance-service and local RSSHub use this skill to fetch enabled subscriptions, filter by source or time window, and present recent articles as a Markdown digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remotely supplied feed URLs may let the skill contact local or internal network services reachable from the agent host.

Mitigation: Restrict allowed feed destinations and review configured RSSHub and feed registry sources before running on machines with private network access.

Risk: RSS titles, summaries, and links are untrusted content that can be placed into an agent-facing Markdown digest.

Mitigation: Treat digest content as data, avoid following embedded instructions from feed text, and review output before using it to drive agent actions.

Risk: Generated cache files can retain fetched feed content and subscription metadata.

Mitigation: Avoid shipping generated cache files and clear caches when packaging or sharing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoocky/skills/quotedance-rss-digest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown digest with article titles, sources, timestamps, links, and short summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports days, limit, source-name filtering, cache refresh, source refresh, and cache clearing options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
