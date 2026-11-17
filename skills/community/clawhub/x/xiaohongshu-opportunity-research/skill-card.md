## Description:

Researches Xiaohongshu search results, post details, creator activity, and public comments so agents can identify market, content, KOL, competitor, and audience-insight opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External operators, marketers, analysts, and agent-workflow developers use this skill to collect public Xiaohongshu keyword, note, creator, and comment data for content research, trend monitoring, competitor analysis, KOL screening, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, note URLs, profile URLs, and related query parameters are sent to guaikei.com with GUAIKEI_API_TOKEN.

Mitigation: Use the skill only when that third-party data flow is acceptable, and avoid private content, account actions, or sensitive profiling tasks.

Risk: Returned public-data results may be saved in local temporary logs.

Mitigation: Review and clear local temp logs according to the user's data-retention expectations, especially after internal analysis work.

Risk: The tool returns public platform data that can support market or KOL judgments but does not make decisions for the user.

Mitigation: Treat results as research inputs and review generated conclusions before using them for marketing, business, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-opportunity-research)
- [Project homepage](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [Guaikei API token service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with Node.js shell commands; command results are structured JSON and may be saved as local temp log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or later and GUAIKEI_API_TOKEN; supports keyword, note URL, and creator profile URL inputs.]

## Skill Version(s):

1.1.4 (source: SKILL.md frontmatter, package.json, references/changelog.md, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
