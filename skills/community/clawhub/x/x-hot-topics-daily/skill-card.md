## Description:

每日追踪并推送 X（x.com）热点话题新闻简报，默认覆盖 AI、LLM、中国社会热点、新加坡社会热点和美国社会热点，并输出反 FOMO 的必知事项、可忽略噪音和 10 分钟行动建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmzo](https://clawhub.ai/user/hmzo)

### License/Terms of Use:


## Use Case:

External users use this skill to have an agent browse X search and trend surfaces with an existing browser session, filter low-quality or suspicious posts, and produce a concise Chinese daily briefing. It is aimed at readers who want fast awareness of AI, LLM, and regional public-interest topics without manually scanning feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads X trends and search results through a browser session, so summaries may reflect rumors, low-quality posts, or misleading engagement signals.

Mitigation: Review the generated briefing for accuracy and source quality before acting on it, especially for breaking news or public-safety topics.

Risk: Using an existing Chrome/X session may expose personalized feed context to the agent during browsing.

Mitigation: Install and run the skill only when browser-based access to the user's X session is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hmzo/skills/x-hot-topics-daily)
- [X Explore](https://x.com/explore/tabs/for_you)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown-style briefing with sections for must-know items, ignorable noise, quick actions, and risk reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes recent X posts, filters likely scams and low-quality rumors, and summarizes selected topics into concise human-facing recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
