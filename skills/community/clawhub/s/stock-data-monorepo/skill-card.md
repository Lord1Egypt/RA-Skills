## Description:

Stock Data Monorepo is a collection of four A-share stock data skills for market volume, top gainers, Tonghuashun themes, and theme-related news events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill collection as a data source for stock-daily-report workflows or for direct A-share market data lookups, including index and volume data, recent top gainers, themes, popularity, and theme event reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses public financial sites and writes local report files.

Mitigation: Run it with an intended output directory, review generated file paths, and avoid exposing secrets in the runtime environment.

Risk: Some helper paths can run mutable external tools, including an npx runtime fallback.

Mitigation: Pin package versions where possible and remove or disable the npx fallback before trusted deployment.

Risk: Under-scoped agent calls may be spawned from user-controlled stock input.

Mitigation: Validate stock codes and constrain subagent inputs before calling the analysis workflows.

Risk: Documented cleanup or reset commands could affect unintended directories or repository state.

Mitigation: Check the target directory and repository state before running destructive cleanup or reset commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinelp100/skills/stock-data-monorepo)
- [README.md](README.md)
- [ths-stock-themes implementation reference](ths-stock-themes/references/implementation.md)
- [Tonghuashun Wencai data source](https://www.iwencai.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON data files, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows browse public financial websites, depend on Python packages, and may write local report files.]

## Skill Version(s):

1.2.5 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
