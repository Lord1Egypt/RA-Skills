## Description:

Zhihu Writer helps agents discover Zhihu trends, select promising topics, analyze competing answers, draft high-engagement Zhihu responses, and create Yanyan short-story submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and content-focused agents use this skill to turn Chinese social-platform trends into structured Zhihu answers, publishing plans, and Yanyan short-fiction drafts. It is intended for topic selection, content drafting, style guidance, tagging, and archive-ready Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch live Zhihu trend data from tophub.today.

Mitigation: Confirm that external network access is acceptable before using trend-fetching workflows.

Risk: The skill produces public-facing draft content for Zhihu answers and Yanyan submissions.

Mitigation: Review drafts for originality, factual support, platform policy compliance, and unwanted disclosure before publishing.

Risk: The skill may save drafts under ~/Documents/notes or ~/Documents/notes/盐言.

Mitigation: Confirm the destination path and file contents before allowing local draft creation.

Risk: Example workflows mention scheduled monitoring.

Mitigation: Create scheduled tasks only after confirming cadence, command behavior, and notification destination.

## Reference(s):

- [Zhihu Writer on ClawHub](https://clawhub.ai/cooperiano/skills/zhihu-writer)
- [Publisher profile](https://clawhub.ai/user/cooperiano)
- [Zhihu trend source](https://tophub.today/n/mproPpoq6O)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and structured prose with tables, outlines, templates, and optional shell commands for scheduled monitoring]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese-language drafts, topic scores, publishing recommendations, tags, archive filenames, and local save paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
