## Description: <br>
Amazon Scraper helps an agent collect Amazon product search data through Apify and generate structured Excel and Markdown reports with product, brand, ASIN, and link details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuokun300](https://clawhub.ai/user/zuokun300) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, marketplace analysts, and ecommerce operators use this skill to gather Amazon search results for product research, competitor monitoring, brand distribution analysis, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid third-party Apify API key for Amazon scraping, which can incur costs or expose credentials if handled carelessly. <br>
Mitigation: Keep the Apify key in an environment variable or secret manager, review Apify cost limits before use, and avoid hardcoding credentials. <br>
Risk: Crawl scope and scheduling can create unexpected volume or policy risk when scraping Amazon results. <br>
Mitigation: Set bounded keyword and product limits, avoid high-frequency scraping, and keep cron or scheduled runs disabled until the crawl scope is reviewed. <br>
Risk: The artifact contains a report-generation defect that can prevent successful output after data collection. <br>
Mitigation: Review and test the scraper in a virtual environment before deployment, and fix the report-generation path before relying on generated reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zuokun300/zuokun300-amazon-scraper) <br>
- [Apify API key setup](https://console.apify.com/account/integrations) <br>
- [README.md](artifact/README.md) <br>
- [USAGE.md](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance plus generated Excel workbooks and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Apify API key and writes timestamped report files to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
