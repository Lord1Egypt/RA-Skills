## Description:

Report-gama helps agents generate country- and category-specific market research reports by gathering multilingual public data across search, news, competitor, ecommerce, advertising, customs, tender, registration, and social sources, then producing charts, Markdown, and PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to request market intelligence for a target country and product category. The skill guides agents through multilingual public data collection, source quality grading, competitive analysis, and final report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses unpinned Python dependencies.

Mitigation: Install and run the skill in a virtual environment or container, and review dependency versions before operational use.

Risk: Broad report requests can trigger long, multi-module public web collection and PDF generation.

Mitigation: Confirm the target country, category, output language, selected modules, report depth, and PDF requirement before running a large report.

Risk: Market reports may include estimates or lower-confidence public-source signals.

Mitigation: Use the skill's source quality grading and cross-check critical market, regulatory, customs, and pricing claims before business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxuan1992asia-svg/skills/reportgama)
- [Publisher profile](https://clawhub.ai/user/wangxuan1992asia-svg)
- [Report-gama HS code reference](artifact/hs_codes.md)
- [Report-gama industry keyword reference](artifact/industry_keywords.md)
- [Report-gama sample test report](artifact/test_report.md)
- [UN Comtrade](https://comtrade.un.org)
- [OEC trade data](https://oec.world)
- [Russian Federal Customs Service](http://www.customs.ru)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports, chart files, PDF exports, command-line examples, and structured research tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can vary by country, category, language, selected modules, depth, and PDF export setting.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
