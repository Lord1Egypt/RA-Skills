## Description:

Generates Chinese-first sports viewing reports for football, basketball, NBA, Premier League, Chinese Super League, Champions League, and other ball sports by organizing public match information, visualizing formations, highlighting players, and presenting source-aware context without making outcome predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmily741963](https://clawhub.ai/user/hmily741963)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sports fans, commentators, educators, and agents use this skill to turn public sports schedules and pre-match context into structured viewing reports, matchup visuals, and refreshable HTML report files. It is intended for legal sports information organization and visualization, not for outcome prediction or betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write generated HTML reports to the desktop and update JSON data files.

Mitigation: Review output paths before execution and prefer no-write or preview modes when refreshing user-maintained JSON.

Risk: The skill may call public sports APIs or user-supplied URLs.

Mitigation: Avoid fetching untrusted URLs and restrict live data collection to known public schedule and sports information sources.

Risk: Generated HTML reports have reported escaping concerns in the security evidence.

Mitigation: Treat report inputs as trusted data until HTML escaping issues are fixed, and review generated reports before sharing.

Risk: Sports context can be misread as outcome prediction or wagering guidance.

Mitigation: Keep outputs limited to public information organization, source tiering, visualization, and explicit no-prediction language.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hmily741963/skills/sport-skill)
- [Analysis Methodology](references/analysis_methodology.md)
- [Data Sources and Tiering](references/data_sources.md)
- [Daily Update Workflow](references/daily_update_workflow.md)
- [Risk and Compliance](references/risk_compliance.md)
- [Professional Analysis Reference](references/professional_analysis.md)
- [Report Template](assets/report_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write HTML reports to the desktop, refresh JSON data files, and use public sports APIs or user-supplied URLs when configured.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 2.9.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
