## Description:

Supports batch keyword expansion workflows for Xiaohongshu-oriented content planning, with multi-depth suggestion generation, deduplication, ranking, and TXT or optional Excel export; current evidence says the suggestions are demo/mock data rather than verified Xiaohongshu autocomplete results.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[otzippo](https://clawhub.ai/user/otzippo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, SEO operators, and content planners can use the skill to run a local batch keyword-expansion script and review generated keyword reports. Because the security evidence says the current release produces demo/mock suggestions, outputs should be treated as workflow examples unless a verified data source is implemented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be mistaken for verified Xiaohongshu autocomplete or trend data.

Mitigation: Label outputs as mock data and do not use them for SEO, competitor, or business decisions until a verified data source is implemented.

Risk: Excel exports created from untrusted keyword inputs may carry spreadsheet safety risk.

Mitigation: Use trusted keyword files and review exported workbooks carefully before opening or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otzippo/skills/xiaohongshu-keyword-batch-autocomplete)
- [Publisher profile](https://clawhub.ai/user/otzippo)
- [Artifact README](README.md)
- [Xiaohongshu website](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; the bundled script writes timestamped TXT reports and optional XLSX workbooks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report rows include keyword text, score, rank, depth, source keyword, reference count, and collection timestamp.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
