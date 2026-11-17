## Description:

Chinese-language Vedic astrology workflow for full chart review, Rashi and Navamsha comparison, past-event review, birth-time stability checks, career themes, marriage and relationship themes, timing windows, location analysis, and structured chart breakdowns from Jagannatha Hora PDFs, screenshots, or text chart data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanding1998](https://clawhub.ai/user/seanding1998)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users and practitioners use this skill to structure Vedic astrology chart analysis, compare divisional charts, review life-event timing, and produce readable Markdown or HTML reports. The workflow emphasizes explicit evidence checks, confidence downgrades when chart data is incomplete, and topic-specific routing for full-chart, career, marriage, and timing/location questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process sensitive birth details and life-context information.

Mitigation: Use only the chart and background information needed for the requested analysis, and avoid retaining generated report files longer than necessary.

Risk: Report mode can create persistent local HTML reports from sensitive personal data.

Mitigation: Choose a dedicated output folder, confirm report creation before writing files, and review generated files before sharing or archiving them.

Risk: The security evidence reports an unsafe-link issue in generated HTML from untrusted Markdown.

Mitigation: Do not open or click links in generated HTML from untrusted Markdown until link scheme filtering is fixed.

## Reference(s):

- [Total Chart Review Workflow](artifact/references/总盘.md)
- [Career Topic Workflow](artifact/references/事业.md)
- [Marriage Topic Workflow](artifact/references/婚姻.md)
- [Timing and Location Workflow](artifact/references/窗口与场域.md)
- [Terminology and Eight-Lens Framework](artifact/references/术语框架.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown analysis with tables, validation summaries, JSON report metadata, shell commands, and optional self-contained HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process sensitive birth and life-context data; report mode can create persistent local HTML files.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
