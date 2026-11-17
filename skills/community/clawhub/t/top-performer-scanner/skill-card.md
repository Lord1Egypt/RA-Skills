## Description:

Finds the true top-performing US stocks per year by downloading NASDAQ-listed symbols, filtering by Top 500 daily dollar volume, and ranking annual returns without survivorship bias.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and quantitative researchers use this skill to identify historical liquid-stock top performers and test whether stock-selection filters would have captured major movers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical market-data results may be incomplete or misleading because the skill depends on NASDAQ FTP and Yahoo Finance data.

Mitigation: Cross-check important findings with an independent market-data source before using them for research conclusions or strategy design.

Risk: Users may mistake historical top-performer analysis for trading advice.

Mitigation: Treat outputs as research only and do not use them to make real trading decisions without independent verification.

Risk: Runtime dependencies and network downloads run in the user's Python environment.

Mitigation: Install and run the skill in a non-privileged virtual environment, and consider pinning dependency versions before use.

## Reference(s):

- [Top Performer Scanner release page](https://clawhub.ai/tltby12341/skills/top-performer-scanner)
- [Publisher profile](https://clawhub.ai/user/tltby12341)
- [NASDAQ Trader symbol directory](ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access for NASDAQ FTP and Yahoo Finance data; get_true_top_500.py writes a CSV file at the configured output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
