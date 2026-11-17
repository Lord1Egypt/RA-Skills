## Description:

When prompted for daily psychology or neuroscience updates in Chinese, this skill searches current Chinese and English authoritative sources and summarizes 10 recent research findings or news items in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2025biophilia-coder](https://clawhub.ai/user/2025biophilia-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request concise Chinese-language daily briefings on psychology and brain science research or news. It helps an agent search, filter, deduplicate, and summarize authoritative sources into a fixed 10-item digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results can be stale, unavailable, or too sparse for an exact same-day psychology and neuroscience digest.

Mitigation: The skill instructs the agent to avoid fabrication, state when same-day public content is unavailable, and label any expanded 7-day results clearly.

Risk: The artifact contains a fixed example date that may become inaccurate for future daily briefings.

Mitigation: Installers should correct the fixed date behavior before use, consistent with the security guidance.

## Reference(s):

- [Source list and search keyword templates](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/2025biophilia-coder/skills/psychology-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-like structured Chinese digest with titles, sources, dates, summaries, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exactly 10 items when enough current sources are available; otherwise it should state that same-day public content was not found and may expand to the previous 7 days.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
