## Description: <br>
智能网页数据采集器。自动识别网页结构，批量抓取列表/表格/详情页数据，支持导出JSON/CSV/Excel。内置反爬策略适配。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjstate](https://clawhub.ai/user/cjstate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams use this skill to run browser-based scraping workflows against authorized sites, define selectors and fields, and export collected list, table, or detail-page data for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs browser automation against arbitrary websites and disables Chromium sandboxing. <br>
Mitigation: Run it in an isolated container or VM, remove or explicitly opt into no-sandbox behavior, and target only sites where scraping is authorized. <br>
Risk: The security scan reports a vulnerable spreadsheet dependency in the dependency set. <br>
Mitigation: Review and update npm dependencies before installation, prefer JSON or CSV export when possible, and handle spreadsheet files as untrusted until dependencies are patched. <br>
Risk: Scraped data may be subject to site terms, robots.txt rules, privacy obligations, or retention controls. <br>
Mitigation: Confirm authorization before collection, use reasonable request delays, and store exported data according to applicable access and data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjstate/xh-smart-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration; scraper exports JSON, CSV, or Excel files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the target site, selectors, export format, and local runtime configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
