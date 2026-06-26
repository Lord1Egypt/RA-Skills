## Description: <br>
Agentic RSS digest using the feed CLI to fetch, triage, and summarize RSS feeds so an agent can surface high-signal posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odysseus0](https://clawhub.ai/user/odysseus0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to catch up on RSS feeds, news, blogs, or recent unread posts and receive a concise digest grouped around high-signal items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external feed CLI and may fetch RSS or article content from network sources selected by configured feeds. <br>
Mitigation: Install only if the user trusts the feed CLI and is comfortable with agent-assisted RSS fetching; ask before importing the starter OPML when automatic default subscriptions are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/odysseus0/rss-digest) <br>
- [feed CLI Go package](https://github.com/odysseus0/feed) <br>
- [Starter OPML feed list](https://github.com/odysseus0/feed/raw/main/hn-popular-blogs-2025.opml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown digest with article summaries and inline shell commands when setup or feed inspection is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference URLs, feed entry identifiers, and selected RSS items; does not mark entries as read by default.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
