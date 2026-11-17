## Description:

Fetches public Xiaohongshu trending-note data with browser automation and can produce daily reports, summaries, and JSON exports for content operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkt-agents](https://clawhub.ai/user/mkt-agents)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to collect public Xiaohongshu trending notes, classify topics, generate concise summaries, and save trend data for daily monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable global npm tooling and an unpinned browser automation runtime can change behavior between installations.

Mitigation: Install in an isolated environment and pin package and browser-runtime versions where possible before operational use.

Risk: Fallback reports may use simulated data when browser automation fails.

Mitigation: Check run logs and saved report metadata before treating exported trend data as live Xiaohongshu data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkt-agents/skills/xiaohongshu-hot-daily)
- [Xiaohongshu public explore page](https://www.xiaohongshu.com/explore)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown-style summaries, and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include fetched note rank, title, author, like count, URL, category, timestamp, and summary text.]

## Skill Version(s):

3.1.0 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
