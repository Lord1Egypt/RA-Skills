## Description:

Stock Tracker monitors Eastmoney self-selected stock announcements, applies rule-based and optional LLM filtering, creates classified summaries, and can present results as scheduled digests or a local web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54lynnn](https://clawhub.ai/user/54lynnn)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agent operators use this skill to track announcements for configured stock groups, filter low-value notices, summarize important updates, and review results through digest output or a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Eastmoney session cookies and LLM API keys.

Mitigation: Use a dedicated environment, restrict access to cookie.txt and .env, and rotate credentials if they may have been exposed.

Risk: The setup script can install recurring cron jobs.

Mitigation: Run scripts/setup.sh only after review and inspect the user crontab after setup.

Risk: The dashboard is unauthenticated and may be reachable beyond localhost if exposed.

Mitigation: Run dashboard mode only on loopback or place it behind access controls.

Risk: LLM features send announcement titles and text to the configured model endpoint and may incur API costs.

Mitigation: Review config.json before use, disable LLM features when not needed, and monitor provider usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/54lynnn/skills/stock-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/54lynnn)
- [System architecture](references/architecture.md)
- [Announcement classification](references/classification.md)
- [Text cleaning rules](references/text-cleaning.md)
- [Token cost analysis](references/token-cost.md)
- [Eastmoney self-selected stocks](https://quote.eastmoney.com/zixuan/lite.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and digest text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dashboard mode can serve local HTML views and CSV exports; scheduled mode emits digest lines for an agent to forward.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
