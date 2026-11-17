## Description:

RSS Digest helps an agent use the feed CLI to fetch, triage, and summarize RSS feeds into high-signal digests of recent posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odysseus0](https://clawhub.ai/user/odysseus0)

### License/Terms of Use:


## Use Case:

Developers, knowledge workers, and external users use this skill to catch up on RSS feeds, blogs, news, and recent posts by having an agent scan entries, select high-signal items, read sources, and synthesize a digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a third-party feed CLI.

Mitigation: Install only from trusted sources, prefer a pinned reviewed CLI version, and avoid elevated privileges.

Risk: The skill fetches RSS feeds and article pages from external sites.

Mitigation: Use it only when external content fetching is acceptable, and review fetched content before acting on it.

Risk: An empty setup may import a public starter feed list automatically.

Mitigation: Confirm the starter feed list is appropriate before importing it into the user environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odysseus0/skills/rss-digest)
- [feed CLI Go package](https://github.com/odysseus0/feed)
- [Starter RSS OPML feed list](https://github.com/odysseus0/feed/raw/main/hn-popular-blogs-2025.opml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown digest with concise summaries and optional inline feed CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent not to mark entries as read unless the user decides to do so.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
