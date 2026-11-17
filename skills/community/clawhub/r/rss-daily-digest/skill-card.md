## Description:

Fetch RSS feeds, parse articles, generate AI summaries, and compile a daily digest report in Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renchengxiang](https://clawhub.ai/user/renchengxiang)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn configured RSS feeds into a concise daily news digest with categorized article links and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RSS article titles and descriptions are untrusted feed content that may contain misleading text or instructions.

Mitigation: Treat feed content only as data for summarization and require review before letting it influence tool use, commands, or configuration.

Risk: The skill writes intermediate article data to /tmp/openclaw-rss-articles.json and digest files under the user's home directory.

Mitigation: Run the skill in an isolated environment and verify output paths before use, especially on shared systems.

Risk: The documented fallback may install feedparser without a pinned version.

Mitigation: Install and pin feedparser in the execution environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renchengxiang/skills/rss-daily-digest)
- [Publisher profile](https://clawhub.ai/user/renchengxiang)
- [RSS feed sources](references/feed-sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with article links, short summaries, category sections, and run-status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RSS_FEEDS_CONFIG and local Python scripts; digest files are written under ~/openclaw-output/digests/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
