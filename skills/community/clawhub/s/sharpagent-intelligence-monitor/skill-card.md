## Description:

SharpAgent Intelligence Monitor is a multi-track intelligence aggregation workflow that collects from RSS, arXiv, GitHub, 36kr, and web search, scores candidates, applies five-factor verification, and produces structured briefings for daily intelligence summaries, tech trend tracking, and competitive monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and teams use this skill to gather public-source AI and technology signals, rank them by relevance and trust, and produce concise daily briefings for trend tracking and competitive monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gathers and summarizes public web sources, so low-confidence or quick-scan items may be incomplete or unverified.

Mitigation: Treat quick-scan items as leads and verify important claims against primary sources before acting on them.

Risk: Dated briefing archives may reveal monitored topics or intelligence priorities if retained locally.

Mitigation: Periodically delete archived briefings when monitored topics are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/sharpagent-intelligence-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/yezhaowang888-stack)
- [36kr hotlist endpoint](https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown briefing with links, ranked sections, scores, signal summaries, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save dated briefing archives locally when used as described by the skill.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
