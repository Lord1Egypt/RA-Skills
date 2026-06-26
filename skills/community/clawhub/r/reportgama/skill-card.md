## Description: <br>
Report-gama helps agents generate country- and category-specific market research reports using multilingual public-source collection, competitive analysis, ecommerce pricing, customs data, tenders, registration checks, social signals, charts, Markdown, and PDF-oriented report outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and analysts use this skill to assemble market intelligence reports for a target country and product category, especially for medical device research across Russia and CIS-oriented sources. It is intended to guide multilingual public-source collection, source quality grading, report structuring, chart generation, and PDF-oriented delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad public web research can run for a long time and collect from many source types. <br>
Mitigation: Confirm the country, product category, language, research depth, source types, and output path before allowing a run. <br>
Risk: The release artifact describes command examples for scripts that are not present in the submitted artifact files. <br>
Mitigation: Review the installed artifact or source package for the referenced scripts before executing the command examples. <br>
Risk: The skill installs several Python packages to support scraping, parsing, charting, and PDF generation. <br>
Mitigation: Install and run it in an isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxuan1992asia-svg/reportgama) <br>
- [Publisher profile](https://clawhub.ai/user/wangxuan1992asia-svg) <br>
- [HS code reference](artifact/hs_codes.md) <br>
- [Industry keyword reference](artifact/industry_keywords.md) <br>
- [Sample generated report](artifact/test_report.md) <br>
- [UN Comtrade](https://comtrade.un.org) <br>
- [OEC](https://oec.world) <br>
- [Russian Federal Customs Service](http://www.customs.ru) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, command examples, structured tables, chart guidance, and PDF-oriented report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on Python 3, pip, public web access, and optional Python packages for parsing, charting, and PDF export.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
