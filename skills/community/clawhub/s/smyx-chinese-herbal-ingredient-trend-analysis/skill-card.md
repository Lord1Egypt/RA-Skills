## Description:

Estimates medicinal-herb active-ingredient accumulation trends from leaf images or videos and provides harvest-timing guidance and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Growers, herb cooperatives, and pharmaceutical raw-material teams use leaf imagery or video to estimate medicinal-herb accumulation trends and inform harvest timing; they can also request cloud-hosted report history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, videos, submitted URLs, identity identifiers, and report-history queries are sent to configured lifeemergence.com services.

Mitigation: Review publisher and service terms before use; avoid confidential farm imagery and internal-only URLs.

Risk: Account and token data may persist locally in a SQLite database.

Mitigation: Use only in workspaces where local token storage is acceptable; review local data handling before installation.

Risk: Reused generic or pet-analysis components and image-based estimates may not suit formal herbal quality assessment.

Mitigation: Review the analysis behavior and confirm harvest or quality decisions with appropriate chemical testing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-chinese-herbal-ingredient-trend-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [Bundled API reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured analysis reports, Markdown history tables, and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual estimates are not chemical assay results; reports may include links to hosted results.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release; bundled SKILL.md states 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
