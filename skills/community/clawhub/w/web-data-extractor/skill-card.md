## Description: <br>
网页数据采集器，支持 CSS 选择器/XPath 提取、批量抓取、自动分页、数据导出（CSV/JSON/Markdown）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[careytian-ai](https://clawhub.ai/user/careytian-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to extract structured data from public web pages with CSS or XPath selectors, handle pagination and batches, and export results for market research, competitive analysis, content aggregation, SEO analysis, and monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports unexplained local command execution access. <br>
Mitigation: Review before installing and prefer deployment only when exec access can be denied, removed, or clearly justified by the publisher. <br>
Risk: Web scraping can violate site rules, overload targets, or collect data the user is not authorized to scrape. <br>
Mitigation: Use only on sites where scraping is authorized, respect robots.txt and site terms, and keep page counts, concurrency, and request rate conservative. <br>
Risk: Export behavior can write scraped data to local files. <br>
Mitigation: Review output filenames and destination paths before writing CSV, JSON, or Markdown exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/careytian-ai/web-data-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/careytian-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Configuration, Guidance] <br>
**Output Format:** [Structured extraction guidance and exported CSV, JSON, or Markdown table files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CSS selectors, XPath selectors, batch URLs, automatic pagination, configurable concurrency, and configurable export format.] <br>

## Skill Version(s): <br>
1.0.0 (source: changelog, config.json, metadata.json, and server release evidence; released 2026-03-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
