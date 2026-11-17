## Description:

Fetch, filter, and summarize RSS/Atom feeds into a clean daily or weekly digest, with support for multiple feeds, keyword filtering, deduplication, and Markdown or plain text output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacjiang](https://clawhub.ai/user/zacjiang)

### License/Terms of Use:


## Use Case:

External users, developers, and content operators use this skill to generate daily or weekly digests from RSS/Atom feeds for briefings, newsletter preparation, monitoring, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted RSS/Atom feeds can supply misleading, malicious, or unsafe content that appears in generated Markdown or text.

Mitigation: Use trusted feed URLs and review generated digest content before forwarding it to agents, newsletters, renderers, or downstream workflows.

Risk: Feed URLs are fetched from the network and could be pointed at private or sensitive endpoints in connected environments.

Mitigation: Restrict feed lists to approved sources, especially on machines or agents that can reach private networks.

Risk: The --output option writes to the specified path and can overwrite existing files.

Mitigation: Choose deliberate non-sensitive output paths and review command arguments before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacjiang/skills/rss-feed-digest)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown or plain text digest, printed to stdout by default or written to a user-specified output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches RSS/Atom feed items, filters by time window and include/exclude keywords, deduplicates by title, and applies a configurable item limit.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
