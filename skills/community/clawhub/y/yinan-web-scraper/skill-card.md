## Description: <br>
Extract structured data from websites using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to extract structured data from websites, including product listings, articles, contact information, prices, job posts, and real estate listings. It supports single-page and paginated scraping workflows and can save results as CSV, JSON, or XLSX files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect website data from targets where scraping is not permitted. <br>
Mitigation: Confirm the target site permits scraping before use and follow site terms and robots.txt expectations. <br>
Risk: Scraping workflows may collect personal or sensitive data. <br>
Mitigation: Avoid collecting personal or sensitive data unless there is a lawful basis and an approved use case. <br>
Risk: Anti-scraping workarounds such as proxies or CAPTCHA-bypass services can create legal, policy, or abuse concerns. <br>
Mitigation: Do not use proxy rotation, CAPTCHA-bypass tactics, or similar measures unless they are clearly authorized. <br>
Risk: User-provided output paths determine where scraped data is written. <br>
Mitigation: Review the output path before running the scripts and store scraped data only in approved locations. <br>


## Reference(s): <br>
- [CSS Selector Reference](references/css-selectors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yinanping-CPU/yinan-web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with inline bash commands; scraper runs can produce CSV, JSON, or XLSX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include requested fields plus scrape metadata such as source URL and scrape timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
