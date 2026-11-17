## Description:

制作天猫店铺经营周报（品牌方沟通版）。使用场景：当用户提供生意参谋、直通车/引力魔方等推广计划报表、客服绩效等数据文件，并要求制作天猫店铺周报时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzbarry1980-bot](https://clawhub.ai/user/gzbarry1980-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and brand teams use this skill to turn Tmall business intelligence, promotion, and customer service data into a brand-facing weekly operations report. The workflow supports metric cleanup, refund and traffic diagnostics, chart generation, Markdown report drafting, and PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chart-generation script uses a hard-coded local output directory, which can write files outside the intended report folder or overwrite prior chart outputs.

Mitigation: Review or change the output directory before running the script, and direct generated charts to the current project or report workspace.

Risk: The workflow depends on store performance, promotion, and customer service data that may be commercially sensitive.

Mitigation: Provide only the data needed for the weekly report and review generated narratives, charts, and exported files before sharing them with brand stakeholders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gzbarry1980-bot/skills/tmall-weekly-report-skill-2)
- [Server-resolved GitHub provenance](https://github.com/gzbarry1980-bot/pinmoo/tree/main/tmp/tmall-weekly-report-skill-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, generated chart image files, Python chart-generation code, shell commands, configuration guidance, and PDF export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured weekly report with 12 standardized charts; chart data and output paths should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
