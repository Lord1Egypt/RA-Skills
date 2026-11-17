## Description:

Read Hacker News with AI summaries in seven supported languages via zeli.app, including daily markdown digests, JSON front-page data, story summary pages, and RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mazzzystar](https://clawhub.ai/user/mazzzystar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch concise Hacker News briefings, topic checks, translated story summaries, and links to original stories or discussions without browsing manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends requests to zeli.app and depends on that third-party service for summaries and translations.

Mitigation: Use it for public Hacker News content, avoid sending private data through requests, and review important summaries against the linked original source or HN discussion.

Risk: Hourly digests and translated summaries may be stale, incomplete, or imperfect.

Mitigation: Respect the documented polling guidance, cache immutable dated digests, and verify high-impact details against primary links before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mazzzystar/skills/zeli-hacker-news)
- [Zeli homepage](https://zeli.app)
- [Zeli LLM context](https://zeli.app/llms.txt)
- [Canonical Zeli skill](https://zeli.app/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON-backed summaries with links and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public Hacker News metadata, summaries, quotes, original links, discussion links, RSS feed references, and translated content from zeli.app.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
