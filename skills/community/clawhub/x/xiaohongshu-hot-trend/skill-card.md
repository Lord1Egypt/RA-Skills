## Description:

Helps agents summarize public Xiaohongshu notes and author pages for keyword, topic, performance, and content theme analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill for user-directed research on public Xiaohongshu notes, author pages, keyword or topic result sets, engagement metrics, and content theme distributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using logged-in browser context or personal pages could expose account-scoped or personal information.

Mitigation: Keep use limited to public or personally authorized pages, and confirm before using logged-in browser context.

Risk: Bulk or high-frequency collection could violate platform rules or trigger anti-abuse controls.

Mitigation: Avoid downloading, interface reverse engineering, and bulk scraping; keep collection lightweight and control request frequency.

Risk: Engagement summaries and manual content classifications can be incomplete or misleading if source pages change or fields are unavailable.

Mitigation: Treat outputs as analysis summaries and verify important claims against the source pages before acting on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/codekungfu/skills/xiaohongshu-hot-trend)
- [Xiaohongshu homepage](https://www.xiaohongshu.com/)
- [Xiaohongshu explore](https://www.xiaohongshu.com/explore)
- [Xiaohongshu search](https://www.xiaohongshu.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include note IDs, author links, topic tags, engagement counts, timing comparisons, and compliance reminders when supported by public page evidence.]

## Skill Version(s):

0.1.0 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
