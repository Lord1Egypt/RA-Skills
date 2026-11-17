## Description:

Searches Xiaohongshu public notes, retrieves note details and comments, and fetches public blogger posts for content research, competitor analysis, KOL screening, and trend insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, data analysts, and agent operators use this skill to collect structured Xiaohongshu public content data for topic research, competitor monitoring, comment insight, and blogger post analysis. It supports downstream summaries, comparisons, screening, and reports after data retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note URLs, profile URLs, and API credentials to the Guaikei service.

Mitigation: Install and run it only when the data-sharing relationship and token use are acceptable for the user's task.

Risk: Generated logs may contain request details or retrieved social-media data.

Mitigation: Treat the logs directory as sensitive, avoid committing or sharing it, and delete logs when they are no longer needed.

Risk: The authoritative security verdict is suspicious because the skill handles API credentials and saved results in ways users should review before installing.

Mitigation: Review the skill and rotate the API token if request URLs, logs, or credentials may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-blogger-posts)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON, markdown, files]

**Output Format:** [Markdown guidance with shell command examples and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results may also be saved under a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter, package.json, and constants report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
