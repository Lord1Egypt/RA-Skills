## Description:

Predict English Premier League football match outcomes first, keep World Cup national-team support for compatibility, include schedule/result context, answer in the user's language, and keep output as statistical reference only, never betting advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datatrevor](https://clawhub.ai/user/datatrevor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request EPL-first football matchup analysis, expected goal difference, schedule or result context, and World Cup national-team compatibility analysis. The skill is for statistical reference only and refuses betting advice, wagering strategy, bookmaker odds, and under-18 use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom WORLDCUP_API_BASE can direct API-key-bearing requests to an arbitrary host.

Mitigation: Use the default https://www.jiajielitong.com service unless you trust the override destination, and avoid permanent SOCCER_API_KEY values with staging or local endpoints.

Risk: The skill depends on a third-party prediction service and publisher-controlled behavior.

Mitigation: Install only if you trust the publisher handle datatrevor and the jiajielitong.com service.

Risk: Football prediction output could be misused as wagering advice.

Mitigation: Treat outputs as statistical references only; keep the disclaimer and refuse betting picks, stake sizing, bookmaker odds, and wagering strategy.

## Reference(s):

- [Football Match Analyzer API Reference](references/api.md)
- [Schedule And Result Reference](references/schedule.md)
- [Canonical Team Names](references/team_names.md)
- [Extended Compliance Notes](references/compliance.md)
- [SoccerAssess API Service](https://www.jiajielitong.com)
- [2026 FIFA World Cup Schedule Reference](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup)
- [2026 FIFA World Cup Schedule Fallback](https://baike.baidu.com/en/item/2026%20FIFA%20World%20Cup/1497370#9)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional shell commands, API-call guidance, bilingual refusal text, and statistical prediction summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the statistical-reference disclaimer, preserve the user's language when possible, and avoid betting advice.]

## Skill Version(s):

1.1.1 (source: frontmatter, release evidence, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
