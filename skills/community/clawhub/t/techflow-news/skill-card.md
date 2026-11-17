## Description:

TechFlow News fetches same-day articles from TechFlow's Chinese site, formats them in a table with links, and summarizes the day's key topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejiming](https://clawhub.ai/user/yejiming)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese-language requests for today's TechFlow news by gathering same-day articles, distinguishing feature posts from 7x24 updates, and producing a short digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic Chinese requests about today's news may invoke this skill even when the user did not specifically ask for TechFlow coverage.

Mitigation: Confirm the requested news source or scope when the user's request is ambiguous.

Risk: The skill reads external webpage content from the disclosed TechFlow URL, so summaries may reflect incomplete, changed, or source-provided information.

Mitigation: Check important claims against the linked TechFlow articles before relying on them.

## Reference(s):

- [TechFlow Chinese site](https://www.techflowpost.com/?lang=zh-CN)
- [ClawHub skill page](https://clawhub.ai/yejiming/skills/techflow-news)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown table and concise prose summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes publication date, article title, brief content summary, full URL, and 3-5 topical highlights.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
