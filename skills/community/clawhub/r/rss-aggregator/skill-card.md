## Description: <br>
Aggregates configured RSS feeds, reads linked articles, merges duplicate events across sources, checks local push history, and produces a concise Markdown news brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HooIla](https://clawhub.ai/user/HooIla) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create repeatable AI news briefings from a configured RSS source list. It is intended for incremental daily pushes that avoid reposting items already recorded in local history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches configured RSS and web sources, so summaries may reflect untrusted or low-quality source content. <br>
Mitigation: Review and curate rss_sources.txt before use, and check generated summaries and links before publishing or forwarding them. <br>
Risk: The skill keeps local pushed_history.log entries so it can avoid repeat pushes. <br>
Mitigation: Inspect, rotate, or clear pushed_history.log when retained feed-processing history is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HooIla/rss-aggregator) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/skill.md) <br>
- [RSS source configuration](artifact/rss_sources.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown news brief with plain-text headings, summaries, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No emoji; each item is formatted as title, summary, and source link entries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
