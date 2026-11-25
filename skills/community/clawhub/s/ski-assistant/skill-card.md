## Description:

Global ski resort assistant covering 854 resorts across 40+ countries for trip planning, price comparison, form analysis, weather checks, and early-bird deal tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjyhahaha](https://clawhub.ai/user/wjyhahaha)

### License/Terms of Use:

MIT-0

## Use Case:

External ski and snowboard users use this skill to choose resorts, estimate trip costs, compare live and reference prices, review ski form, track presale opportunities, and prepare for trips in Chinese or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local profile, trip, watchlist, price-history, and coaching-history files that may contain personal travel and activity data.

Mitigation: Review the local data directory, limit saved details to what is needed, and delete stored records when they are no longer useful.

Risk: Live search, weather, exchange-rate, resort discovery, and flyai workflows can send queries to external services.

Mitigation: Use live-data features only when needed, avoid placing sensitive personal details in search queries, and disclose when a source is unavailable or degraded.

Risk: Reminder workflows can create scheduled reminders after user consent, which may surprise users if settings are not reviewed.

Mitigation: Confirm reminder timing and channels before creating reminders, and review platform reminder settings after setup.

Risk: Database update workflows can replace the local resort database from an upstream source.

Mitigation: Run database updates only when the upstream source is trusted, keep the backup file, and review changed or newly marked records before relying on them.

## Reference(s):

- [Ski Assistant README](README.md)
- [Search Strategies Maintenance Report](docs/strategies_maintenance_report.md)
- [Budget Templates](references/budget-templates.md)
- [Coaching Rubric](references/coaching-rubric.md)
- [Gear Guide](references/gear-guide.md)
- [Pre-Departure Checklist](references/pre-departure-checklist.md)
- [Resorts Reference](references/resorts-reference.md)
- [Travel Guide](references/travel-guide.md)
- [Noto CJK Fonts](https://github.com/googlefonts/noto-cjk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown reports and tables, JSON state files, shell commands for helper tools, and optional generated share-card image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label price sources, disclose degraded live-data paths, and include safety reminders for trip planning and pricing responses.]

## Skill Version(s):

7.0.0 (source: server release metadata, SKILL.md frontmatter, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
