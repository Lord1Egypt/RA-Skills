## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data with portfolio management, watchlist alerts, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run command-line stock and cryptocurrency analysis, portfolio tracking, watchlist alerts, dividend checks, hot-trend scans, and rumor or early-signal scans for informational investing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanners can load live X session cookies from .env and pass the broader process environment to an external Bird CLI.

Mitigation: Use --no-social for hot scans when social data is not required, avoid storing unrelated secrets in the skill .env, and only enable Bird CLI after reviewing its installation and credential handling.

Risk: Financial signals, rumor scoring, and trend scans can be stale, incomplete, or misleading and are not financial advice.

Mitigation: Use results for informational screening only, verify important claims against primary market sources, and consult a licensed financial advisor before acting on investment decisions.

Risk: The scripts can write local portfolio, watchlist, cache, and output JSON files.

Mitigation: Run the skill in a workspace where local state files are expected, and inspect generated files before sharing logs or reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/test-0612)
- [Publisher Profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [Usage Guide](docs/USAGE.md)
- [Technical Architecture](docs/ARCHITECTURE.md)
- [Hot Scanner](docs/HOT_SCANNER.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text and JSON reports, with Markdown documentation and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, cache, and scanner output JSON files when the corresponding scripts are run.]

## Skill Version(s):

6.2.0 (source: SKILL.md frontmatter); ClawHub release version 1.0.1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
