## Description:

研林Skill - 财经新闻采集+关键事件筛选过滤，只保留有实质影响的事件.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts, investment researchers, and agents use this skill to fetch Sina Finance headlines and keep the items that appear materially relevant to markets, sectors, or policy. It returns a concise ranked list of Chinese-language financial events with importance scores and sector mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Sina Finance over the network, which may conflict with strict network allowlists.

Mitigation: Review network access requirements before installation and restrict execution to environments where the Sina Finance endpoint is permitted.

Risk: The skill produces Chinese-language output and uses keyword-based filtering, so results may omit relevant headlines or include low-signal items.

Mitigation: Review filtered events before using them in investment research or operational workflows, and adapt keywords or output handling when non-Chinese output is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanlin-news-filter)
- [Sina Finance news feed endpoint](https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=30&page=1&r=0.1)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Chinese-language plain text summary or JSON event list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks up to eight filtered events by keyword-based importance and includes source, importance, sector mapping, and marginal-event flags.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
