## Description:

Start every day focused. Get a morning briefing with overdue tasks, today's priorities, calendar overview, and context from recent meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual operators use this skill to turn workspace to-dos, recent meeting notes, calendar context, and optional memory files into a concise daily or weekly planning briefing. It helps identify overdue work, today's priorities, schedule context, and a single focus item.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily briefings may expose private workspace to-dos, recent meeting notes, calendar details, memory files, or user preference files.

Mitigation: Install only when that context is appropriate for briefing use, invoke the skill explicitly, and avoid storing secrets or unrelated sensitive facts in files the skill may read.

Risk: Priority and focus recommendations may be incomplete when the workspace lacks current to-do, meeting, calendar, or memory context.

Mitigation: Treat the briefing as planning guidance and verify high-impact deadlines, meetings, and obligations against authoritative sources before acting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/quincygunter/skills/quincy-ai-daily-briefing)
- [Author homepage](https://jeffjhunter.com)
- [Quick Start: AI Daily Briefing](artifact/examples/quick-start.md)
- [Example Output: Daily Briefing](artifact/examples/output-example.md)
- [Briefing Preferences](artifact/assets/PREFERENCES-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown briefing with ordered sections, checklists, bullets, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize workspace tasks, recent meeting notes, calendar details, and optional memory or preference files when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
