## Description:

reportgama2 generates deep market research reports for a selected country and product category using multilingual public-source collection across search, news, competitors, ecommerce pricing, advertising, customs, tenders, registrations, social platforms, medical organizations, and reference pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market researchers use this skill to run configurable market intelligence collection for a target country and product category and produce a structured report. It is especially oriented toward multilingual medical-device and regional-market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad outbound public web and social-platform collection.

Mitigation: Run it only in environments where outbound research traffic is acceptable, and confirm country, category, modules, output location, and language before a full run.

Risk: The install path uses mutable Python dependencies.

Mitigation: Use a virtual environment and pin or review dependency versions before operational use.

Risk: Social-platform and public-source results may contain personal, regulated, or low-confidence information.

Mitigation: Treat results as public-source intelligence, review source quality, and sanitize sensitive content before sharing reports.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wangxuan1992asia-svg/skills/reportgama2)
- [HS codes reference](artifact/references/hs_codes.md)
- [Industry keywords reference](artifact/references/industry_keywords.md)
- [UN Comtrade](https://comtrade.un.org)
- [The Observatory of Economic Complexity](https://oec.world)
- [Russian Federal Customs Service](http://www.customs.ru)
- [Roszdravnadzor](https://roszdravnadzor.gov.ru)
- [GRLS medicine register](https://grls.rosminzdrav.ru)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, optional PDF files, charts, and structured research data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local report, chart, and data files based on selected modules, country, category, language, and output path.]

## Skill Version(s):

1.0.0 (source: server release; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
